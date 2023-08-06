# SimpleTap

## Configuration
The configuration file is a JSON file in the config directory in the user's profile. Here is an example:
```JSON
{
    "servers": [
        [
            "1.sts.benmickler.com",
            5623
        ]
    ],
    "benmickler.simpletap.switchbox.switches": {
        "switchbox_name": "SimpleTap switchbox",
        "auto_connect": true
    },
    "benmickler.simpletap.rfid.mfrc522": {
        "scan_delay": 0.75
    },
    "extensions": {
        "disabled": [
            "benmickler.simpletap.rfid.mfrc522"
        ],
        "auto_start": true
    },
    "package_manager": {
        "repositories": [
            {
                "url": "packages.st.benmickler.com",
                "auto update": true,
                "auto upgrade apps": true,
                "auto upgrade packages": true,
                "auto upgrade system": true,
                "auto upgrade extensions": true
            }
        ]
    },
    "benmickler.simpletap.tts.polly": {
        "aws_access_key_id": "[YOUR AWS ACCESS KEY ID]",
        "aws_secret_access_key": "[YOUR AWS SECRET ACCESS KEY]",
        "voices": {
            "en": "Olivia",
            "de": "Vicki"
        },
        "output_format": "mp3",
        "region_name": "ap-southeast-2"
    },
    "main app": "benmickler.simpletap.main"
}
```