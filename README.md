all credit to https://ladis.cloud/blog/posts/firmware-update-8bitdo.html

# How to update the firmware of 8BitDo's gamepads without using Upgrade Tools

In the past 8BitDo offered the firmware files for their gamepads as downlodable ZIP archives on their [support site](https://support.8bitdo.com/). But for their more recent versions, the Upgrade Tool is required in order to download and flash the firmware onto their gamepads. Unfortunately there is no native linux version of the Upgrade Tool available as of today.

If you want to know how to still download and flash their latest firmware versions continue reading.

## Download the firmware file

First get a listing of the available firmware files. To do this, issue a HTTP POST request to 8BitDo's new download API. An additional header my be used to filter for a specific gamepad.

For example:

```bash
$ curl -X POST -H 'Type: 9' -H 'Beta: 1' http://dl.8bitdo.com:8080/firmware/select
```

The following table shows the currently available gamepad types:

| Gamepad | Type |
|---|---|
| Arcade Stick | 34 |
| Arcade Stick Receiver | 35 |
| F30 GamePad | 2 |
| F30 Arcade Stick | 5 |
| F30 Pro | 1 |
| Lite GamePad | 28 |
| M30 | 23 |
| N30 GamePad | 2, 10 |
| N30 NS GamePad | 18 |
| N30 Pro | 1 |
| N30 Pro 2 | 13 |
| Pro 2 | 33 |
| Pro 2 Wired | 37 |
| SF30 Pro | 9 |
| SN30 GamePad | 3, 17 |
| SN30 Pro+ | 25 |
| SN30 Pro | 9 |

The download API will send a JSON that will look like this:

```json
{
  "msgState": 1,
  "error": "",
  "list": [{
    "date": "2021-04-19",
    "fileName": "SN30pro+SF30pro",
    "type": 9,
    "version": 1.3600000143051147,
    "winDownload": 8725,
    "fileSize": 89116,
    "filePathName": "/firmwareFile/upload/cab12b12-8e01-472f-a9f4-ec2237c598b9.dat",
    "beta": "",
    "md5": "78F7D5CCCA6C2FD6A9644616BD3E7F52"
  }, {
    ...
  }]
}
```

The `filePathName` property contains the path name of the firmware file we need to download.

Make sure to choose the correct version:

```bash
$ curl -X GET -O http://dl.8bitdo.com:8080/firmwareFile/upload/cab12b12-8e01-472f-a9f4-ec2237c598b9.dat
```

## Flashing the firmware file on the gamepad

The `fwupd` tool is required to flash the firmware files on 8BitDo's gamepads. Start your gamepad by holding down L(1)+R(1)+START for 3 seconds. A status LED on the gamepad should now blink red. Then connect the gamepad to the computer with a USB cable.

The gamepad should now show up in the `fwupd` tool:

```bash
$ fwupdmgr get-devices
├─ 8Bitdo:
│ Device ID: 23ec719b6aabc2d2dac5176c232f0da7a21881b0
│ Summary: A redesigned classic game controller
│ Current version: 1.34
│ Vendor: 8BitDo
│ Device Flags: • Updatable
│ • Is in bootloader mode
...
```

The device id is then used to flash the firmware file on this gamepad:

```bash
$ fwupdtool install-blob cab12b12-8e01-472f-a9f4-ec2237c598b9.dat 23ec719b6aabc2d2dac5176c232f0da7a21881b0
```

The `fwupd` tool may fail to restart the gamepad after writing the firmware. If it times out, restart the gamepad and verify that the firmware was updated correctly.
