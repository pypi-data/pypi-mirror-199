##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides the Scientific Data Container as class
# DataContainer which may be stored or uploaded as a ZIP package
# containing items (files). Do not use this class directly! Use the
# class Container provided by the package scidatacontainer instead.
#
##########################################################################

import copy
import hashlib
import io
import json
import requests
import time
import uuid
from zipfile import ZipFile

from .filebase import FileBase, TextFile, JsonFile
from .config import load_config
config = load_config()

# Version of the implemented data model
MODELVERSION = "0.6"


##########################################################################
# Timestamp function

def timestamp():

    """ Return the current ISO 8601 compatible timestamp string. """

    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime(time.time()))


##########################################################################
# Data container class

class DataContainer(object):

    """ Scientific data container with minimal file support. """

    _config = config
    _suffixes = {"json": JsonFile, "txt": TextFile, "bin": FileBase}
    _classes = {dict: JsonFile, str: TextFile, bytes: FileBase}
    _formats = [TextFile]


    def __init__(self, items=None, file=None, uuid=None, server=None, key=None):

        # Container must be mutable initially
        self.mutable = True

        # Store all items in the container
        if items is not None:
            self._store(items, True, False)
            self.mutable = not self["content.json"]["static"]

        # Load local container file
        elif file is not None:
            self._read(fn=file)

        # Download container from server
        elif uuid is not None:
            self._download(uuid=uuid, server=server, key=key)

        # No data source
        else:
            raise RuntimeError("No data!")


    def _store(self, items, validate=True, strict=True):

        """ Store all items in the container. """

        # Add all items in the container
        self._items = {}
        mutable = self.mutable
        self.mutable = True
        for path, data in items.items():
            self[path] = data

        # Make sure that the items content.json and meta.json exist and
        # contain all required attributes
        if "content.json" not in self:
            raise RuntimeError("Item 'content.json' is missing!")
        if "meta.json" not in self:
            raise RuntimeError("Item 'meta.json' is missing!")
        if validate:
            self.validate_content()
            self.validate_meta()

        # Check validity of hash
        if strict and self["content.json"]["hash"]:
            oldhash = self["content.json"]["hash"]
            self.hash()
            if self["content.json"]["hash"] != oldhash:
                raise RuntimeError("Wrong hash!")

        # Restore mutable flag
        self.mutable = mutable


    def __contains__(self, path):

        """ Return true, if the given path matches an item in this
        container. """

        return path in self._items
    
        
    def __setitem__(self, path, data):

        """ Store data as a container item. """

        # Immutable container must not be modified
        if not self.mutable:
            raise RuntimeError("Immutable container!")
        
        # Get file extension
        ext = path.rsplit(".", 1)[1]

        # Unregistered file extension
        if not ext in self._suffixes:

            # Try to convert bytes. Default is FileBase.
            if isinstance(data, bytes):
                for cls in self._formats:
                    try:
                        item = cls(data)
                        break
                    except:
                        pass
                else:
                    item = FileBase(data)

            # Other Python object must be registered
            else:
                if type(data) in self._classes:
                    cls = self._classes[type(data)]
                    item = cls(data)
                else:
                    raise RuntimeError("No matching file format found for item '%s'!" % path)

        # Registered file extension         
        else:
            cls = self._suffixes[ext]
            item = cls(data)

        # Store conversion object containing data
        self._items[path] = item
##        print("**** Class('%s') = %s ****" % (path, type(item).__name__))


    def __getitem__(self, path):

        """ Get the data content of a container item. """

        if path in self:
            return self._items[path].data
        raise KeyError("Unknown item '%s'!" % path)


    def validate_content(self):

        """ Make sure that the item "content.json" exists and contains
        all required attributes. """

        # Get a copy of the item "content.json"
        content = copy.deepcopy(self["content.json"])

        # Keep UUID of a multi-step container and create a new one otherwise
        if "uuid" not in content or not content["uuid"]:
            content["uuid"] = str(uuid.uuid4())

        # The optional attribute 'replace' contains the UUID of the
        # predecessor of this container. It replaces the former one,
        # which must have the same containerType and owner and a smaller
        # or equal creation time. The replacement feature should only be
        # used for minor data modifications (e.g. additional keywords or
        # comment in meta.json). The server returns always the latest
        # version.
        if "replaces" not in content:
            content["replaces"] = None

        # The attribute 'containerType' is a dictionary which must at
        # least contain the type of the container as short string
        # without spaces. If the container type is standardized, it must
        # also contain a type id and a version string.
        if "containerType" not in content:
            raise RuntimeError("Attribute 'containerType' is missing!")
        ptype = content["containerType"]
        if not isinstance(ptype, dict):
            raise RuntimeError("Attribute containerType is no dictionary!")
        if "name" not in ptype:
            raise RuntimeError("Name of containerType is missing!")
        if "id" in ptype and not "version" in ptype:
            raise RuntimeError("Version of containerType is missing!")

        # The boolean attribute 'static' is required. Default is False.
        if "static" in content:
            content["static"] = bool(content["static"])
        else:
            content["static"] = False

        # The boolean attribute 'complete' is required. Default is True.
        if not content["static"] and "complete" in content:
            content["complete"] = bool(content["complete"])
        else:
            content["complete"] = True

        # Current time
        ts = timestamp()

        # The attribute 'created' is required. It is created
        # automatically for a new dataset.
        if "created" not in content or not content["created"]:
            content["created"] = ts

        # The attribute 'modified' is updated automatically for a
        # multi-step dataset
        if "modified" not in content or not content["complete"]:
            content["modified"] = ts

        # The attribute 'hash' is optional
        if "hash" not in content or not content["hash"]:
            content["hash"] = None

        # The attribute 'usedSoftware' is a list of dictionaries, which
        # may be empty. Each dictionary must contain atleast the items
        # "name" and "version" specifying name and version of a
        # software. It may also contain the items "id" and "idType"
        # specifying a reference id (e.g. GitHub-URL) and its type.
        if "usedSoftware" not in content or not content["usedSoftware"]:
            content["usedSoftware"] = []
        for sw in content["usedSoftware"]:
            if not "name" in sw:
                raise RuntimeError("Software name is missing!")
            if not "version" in sw:
                raise RuntimeError("Software version is missing!")
            if "id" in sw and not "idType" in sw:
                raise RuntimeError("Type of software reference id is missing!")

        # Version of the data model provided by this package
        content["modelVersion"] = MODELVERSION

        # Store the item "content.json"
        self["content.json"] = content
        

    def validate_meta(self):
        
        """ Make sure that the item "meta.json" exists and contains
        all required attributes. """

        # Get a copy of the item "meta.json"
        meta = copy.deepcopy(self["meta.json"])

        # Author name is required
        if "author" not in meta:
            meta["author"] = self._config["author"]
        if not meta["author"]:
            raise RuntimeError("Author name is missing!")

        # Author email address is required
        if "email" not in meta:
            meta["email"] = self._config["email"]

        # Author affiliation is optional
        if "organization" not in meta:
            meta["organization"] = ""

        # Comment on dataset is optional
        if "comment" not in meta:
            meta["comment"] = ""

        # Title of dataset is required
        if "title" not in meta:
            meta["title"] = ""
        if not meta["title"]:
            raise RuntimeError("Data title is missing!")

        # List of keywords is optional
        if "keywords" not in meta:
            meta["keywords"] = []

        # Description of dataset is optional
        if "description" not in meta:
            meta["description"] = ""

        # Data creation time is optional
        if "timestamp" not in meta:
            meta["timestamp"] = ""

        # Data DOI is optional
        if "doi" not in meta:
            meta["doi"] = ""

        # Data license name is optional
        if "license" not in meta:
            meta["license"] = ""

        # Store the item "meta.json"
        self["meta.json"] = meta


    def __delitem__(self, path):

        """ Delete the given item. """

        # Immutable container must not be modified
        if not self.mutable:
            raise RuntimeError("Immutable container!")

        # Delete item        
        if path in self:
            del self._items[path]
            

    def keys(self):

        """ Return a sorted list of the full paths of all items. """

        return sorted(self._items.keys())


    def values(self):

        """ Return a list of all item objects. """

        return [self[k] for k in self.keys()]


    def items(self):

        """ Return this container as a dictionary of item objects. """

        return {k: self[k] for k in self.keys()}


    def hash(self):

        """ Calculate hash value of this container. """

        # Some attributes of content.json are excluded from the hash
        # calculation
        save = ("uuid", "created", "modified")
        save = {k: self["content.json"][k] for k in save}
        for key in save:
            self["content.json"][key] = None
        self["content.json"]["hash"] = None

        # Calculate and store hash of this container
        hashes = [self._items[p].hash() for p in sorted(self.items())]
        myhash = hashlib.sha256(" ".join(hashes).encode("ascii")).hexdigest()
        self["content.json"]["hash"] = myhash

        # Restore excluded attributes
        for key, value in save.items():
            self["content.json"][key] = value

        # Make container immutable
        self.mutable = False


    def freeze(self):

        """ Calculate the hash value of this container and make it
        static. The container cannot be modified any more when this
        method was called once. """

        self["content.json"]["static"] = True
        self["content.json"]["complete"] = True
        self.hash()


    def release(self):

        """ Make this container mutable. If it was immutable, this
        method will create a new UUID and initialize the attributes
        replaces, created, modified and modelVersion in the item
        "content.json". It will also delete an existing hash and make it
        a single-step container. """

        # Do nothing if the container is already mutable
        if self.mutable:
            return
        self.mutable = True
        
        # Remove and initialize certain container attributes
        content = self["content.json"]
        content["static"] = False
        content["complete"] = True
        for key in ("uuid", "replaces", "created", "modified", "hash"):
            content.pop(key, None)
        self.validate_content()
        

    def encode(self):

        """ Encode container as ZIP package. Return package as binary
        string. """

        items = {p: self._items[p].encode() for p in self.items()}
        with io.BytesIO() as f:
            with ZipFile(f, "w") as fp:
                for path in sorted(items.keys()):
                    fp.writestr(path, items[path])
            f.seek(0)
            data = f.read()
        return data
    

    def decode(self, data, validate=True, strict=True):

        """ Take ZIP package as binary string. Read items from the
        package and store them in this object. """
        
        with io.BytesIO() as f:
            f.write(data)
            f.seek(0)
            with ZipFile(f, "r") as fp:
                items = {p: fp.read(p) for p in fp.namelist()}
        self._store(items, validate, strict)

        
    def write(self, fn, data=None):

        """ Write the container to a ZIP package file. """

        if data is None:
            data = self.encode()
        with open(fn, "wb") as fp:
            fp.write(data)
        self.mutable = not (self["content.json"]["static"] or self["content.json"]["complete"])


    def _read(self, fn, strict=True):

        """ Read a ZIP package file and store it as container in this
        object. """

        with open(fn, "rb") as fp:
            data = fp.read()
        self.decode(data, False, strict)
        self.mutable = not (self["content.json"]["static"] or self["content.json"]["complete"])


    def upload(self, data=None, strict=True, server=None, key=None):

        # Server name is required and must be provided either via config
        # file, environment variable or method parameter
        if server is None:
            server = self._config["server"]
        if not server:
            raise RuntimeError("Server URL is missing!")

        # API key is required and must be provided either via config
        # file, environment variable or method parameter
        if key is None:
            key = self._config["key"]
        if not key:
            raise RuntimeError("Server API key is missing!")

        # Upload container as byte string
        if data is None:
            data = self.encode()
        try:
            response = requests.post(server + "/api/datasets/",
                                     files={"uploadfile": data},
                                     headers={"Authorization": "Token " + key})
        except:
            response = None
        if response is None:
            raise ConnectionError("Connection to server %s failed!" % server)

##        print("*** Debug file 'upload.zdc' ***")
##        with open("upload.zdc", "wb") as fp:
##            fp.write(response.content)

        # HTTP status code 409 is returned when a dataset is already
        # available on the server. Static datasets require a special
        # treatment: The current dataset is replaced by the one from the
        # server.
        if response.status_code == 400:
            if self["content.json"]["static"]:
                data = json.loads(response.content.decode("UTF-8"))
                if isinstance(data, dict) and data["static"]:
                    self._download(uuid=data["id"], server=server, key=key)
                    return
            raise requests.HTTPError("400 Bad Request: Invalid container content")

        # Unauthorized access
        elif response.status_code == 403:
            raise requests.HTTPError("403 Forbidden: Unauthorized access")

        # Duplicate UUID
        elif response.status_code == 409:
            raise requests.HTTPError("409 Conflict: UUID is already existing")

        # Invalid container format
        elif response.status_code == 415:
            raise requests.HTTPError("415 Unsupported: Invalid container format")

        # Standard exception handler for other HTTP status codes
        else:
            response.raise_for_status()

        # Make container immutable
        self.mutable = not (self["content.json"]["static"] or self["content.json"]["complete"])


    def _download(self, uuid, strict=True, server=None, key=None):

        # Server name is required and must be provided either via config
        # file, environment variable or method parameter
        if server is None:
            server = self._config["server"]
        if not server:
            raise RuntimeError("Server URL is missing!")
        
        # API key is required and must be provided either via config
        # file, environment variable or method parameter
        if key is None:
            key = self._config["key"]
        if not key:
            raise RuntimeError("Server API key is missing!")

        # Download container as byte stream from the server
        try:
            response = requests.get(server + "/api/datasets/" + uuid + "/download/",
                                    headers={"Authorization": "Token " + key})
        except:
            response = None
        if response is None:
            raise ConnectionError("Connection to server %s failed!" % server)
        data = response.content

##        print("*** Debug file '%s.zdc' ***" % uuid)
##        with open(uuid+".zdc", "wb") as fp:
##            fp.write(data)

        # Valid dataset: Store in this container
        if response.status_code == 200:
            self.decode(data, False, strict)
            
        # Deleted dataset: Raise exception
        elif response.status_code == 204:
            raise requests.HTTPError("204 No Content: Deleted dataset")
            
        # Replaced dataset: Store in this container
        elif response.status_code == 301:
            self.decode(data, strict)
            
        # Unauthorized access
        elif response.status_code == 403:
            raise requests.HTTPError("403 Forbidden: Unauthorized access")

        # Unknown dataset: Raise exception
        elif response.status_code == 404:
            raise requests.HTTPError("404 Not Found: Unknown dataset")
            
        # Standard exception handler for other HTTP status codes
        else:
            response.raise_for_status()

        # Make container immutable
        self.mutable = not (self["content.json"]["static"] or self["content.json"]["complete"])


    def __str__(self):

        content = self["content.json"]
        meta = self["meta.json"]

        if content["static"]:
            ctype = "Static Container"
        elif content["complete"]:
            if content["created"] == content["modified"]:
                ctype = "Single-Step Container"
            else:
                ctype = "Closed Multi-Step Container"
        else:
            ctype = "Open Multi-Step Container"

        s = [ctype]
        ptype = content["containerType"]
        name = ptype["name"]
        if "id" in ptype:
            name = "%s %s (%s)" % (name, ptype["version"], ptype["id"])
        s.append("  type:     " + name)
        s.append("  uuid:     " + content["uuid"])
        if content["replaces"]:
            s.append("  replaces: " + content["replaces"])
        if content["hash"]:
            s.append("  hash:     " + content["hash"])
        s.append("  created:  " + content["created"])
        if "Multi" in ctype:
            s.append("  modified: " + content["modified"])
        s.append("  author:   " + meta["author"])

        return "\n".join(s)        
