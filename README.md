# `vrms` for ArchLinux

Enumerates non-free packages (that is to say, under licenses not considered by OSI, FSF, and/or the DFSG to be Free Software) installed on an Arch Linux system. See [`license_finder.py`](src/vrms_arch/license_finder.py) for the license categorization.

A reimplementation of the original [`vrms`](http://vrms.alioth.debian.org/) program from Debian for Arch's Pacman and ALPM.

## Usage

List non-free packages (and count currently ambiguous/uncheckable packages, see Caveats)

```sh
vrms
```
    
Check all packages in locally synced package repositories (typically does not include the AUR), not just locally installed packages:

```sh
vrms --global-repos
```

## Installing

Easiest way is to use the "official" AUR package: [vrms-arch-git](https://aur.archlinux.org/packages/vrms-arch-git)

### From source

Build a package out of local checkout of this source code on Arch:

```sh
git clone https://github.com/gardenappl/vrms-arch
cd vrms-arch
makepkg -si --noextract
```
    
This works because `makepkg` treats `src/` as the package source directory, while the `PKGBUILD` contains instructions to `cd ..` where the build command can find the needed `setup.cfg` and `.toml` files.

## Caveats

A great deal of packages in Arch, both free and non-free, use `custom` as the license field value. As per the [Arch package guidelines](https://wiki.archlinux.org/index.php/Arch_package_guidelines#Licenses), this indicates that the package does not use an exact copy of one of the licenses included in the core [`licenses` package](https://www.archlinux.org/packages/core/any/licenses/), which provides well-known free licenses at `/usr/share/licenses/common`.

Many commonly used Free Software licenses aren't included in the common `licenses` package because they require editing to be applied to a given project, such as the BSD and MIT licenses.

However, the guidelines go on to say that the license field can be disambiguated in the form of `custom: MIT` or `custom: ZLIB`. Sadly, there are many packages in the Arch Linux repositories that specify only `custom`.

You can list all "ambiguous" packages with:

```sh
vrms --list-unknowns
```

If you're certain that these packages are FOSS, you may add them to the ["disambiguation database"](src/vrms_arch/disambiguation.py) and submit a pull request.

Many packages also carelessly use variant naming of well-known licenses (`GPL-2`, `GPLv2`, etc.) in spite of the package guidelines, causing further confusion. `vrms` will try to "clean up" variant names by removing dashes, underscores, turning all letters into lowercase, etc., however, this is not a perfect solution.

The same problems apply to AUR packages.
