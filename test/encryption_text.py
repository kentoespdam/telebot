import importer_test
from services.encryption import encode, decode

print(f"gis@8833    : {encode('gis@8833')}")
print(f"purwo       : {encode('purwo')}")
print(f"password    : {encode('password')}")


print(f"gis@8833    : {decode('gAAAAABlcYcQhQ5sml3rcGOBraolrK76mEcIbHPHDeCt9w0l83jNGfgMyH-RKwz2NJd0G47kwTxxqcYpirkZOV6nTT5tnxJpoA==')}")
print(f"password    : {decode('gAAAAABlcYcQq5E-5Q9OBbhnIXPb4QnIZxuGbhvKAXCO0DXD8wkYRep16nMmGyXfGHG2feuvXsH_HY0Cc2truVwoH0Ko5rTxpA==')}")