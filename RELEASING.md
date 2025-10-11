# Performing a Release of the MicroLab

The MicroLab is an open source hardware/software project with many moving parts. This document is a concise guide for how to go about creating a releasing a stable version.

## Preparing for Release

- Build the latest disk image using [the scripts here](https://github.com/FourThievesVinegar/microlab-image/blob/main/BUILD.md).
- Perform end-to-end testing on a completed unit. Typically this will mean running a test recipe such as Caffeine Extraction on an assembled unit. A mock unit can also be used (for example, one that switches LED's instead of running pumps and motors) but nothing brings out the bugs like a real-life test that does some sort of actual chemistry.
- Make sure that documentation is up to date, including the main README.md, CHANGELOG.md, and any instructions in the docs folder.

### Removing extraneous data

If you are shipping or imaging a device you have logged into and messed with, you may want to remove your development bash history. You can do so with the following command:

```bash
history -c && history -w
```

You may want to remove wifi networks you have logged into. Check `/etc/wpa_supplicant/wpa_supplicant.conf` for saved networks and delete any that you don't want people to know about.

## Doing the Release

- Make a stable branch off of `main`, cherry-pick to it if you make last-minute changes. Use a name like v0.6.0 or v1.0. Use semantic versioning.
- Update version numbers in files as appropriate and update the CHANGELOG document as well.
- Make a release tag for your branch on GitHub.
