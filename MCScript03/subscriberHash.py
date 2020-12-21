import hashlib  # A standard library that does hashes

def subHashGen(emailString):
    # The following is in .lower() case because mailchimp forms
    # hashes from lowercase strings.
    # The .encode() method tagged on the end encodes it as a byte literal
    emailByte = emailString.lower().encode(encoding="utf-8")

    # This uses the hashlib library to make the hash. The .hexdigest()
    # seems to be about equivalent to str() [forgive me internet!]
    subHash = hashlib.md5(emailByte).hexdigest()
    return subHash

#print(subHashGen("Urist.McVankab@freddiesjokes.com")=="62eeb292278cc15f5817cb78f7790b08")