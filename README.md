<p align="center">
    <img src="https://storage.googleapis.com/replit/images/1654232400062_57239fe5995715e769a2e88f9131ee72.png" width="128px" alt="forge logo"/>
</p>

<h1 align="center">Minecraft Forge Server Hosting Utils</h1>
I created these utilities to make modded minecraft server hosting less painful.

> Supports only mods from CurseForge!

## You Get
- Automated mod downloading and updating
- Server hosted using Docker
- Easily accessible server configuration files

## How To Use
### Server
1. Bulild the Docker image
```sh
docker-compose build
```
2. Start the server
```sh
docker-compose up
```
3. Stop the server
```sh
docker-compose down
```
> Make sure you have Docker and Docker Compose installed on your system before running these commands.

### Mods
There are 3 scripts available.

`update-index.py` - creates an index out of `mods.txt` file containing all links to mods

> Index is a special file that contains all the information needed by the script to download the mods. After creation it is placed in `mods/index.txt`.

`sync.py` - parses the index and downloads mods. It doesn't redownload mods that are already present. It also deletes mods that are no longer needed.

`compile.py` - creates `out/sync.bat` file which is `sync.py` script wrapped in magical code that with a little bit of hackery gives us the possibility of running everything by double clicking the file.

#### Workflow
1. Customize the mods in the `mods.txt` file
2. Run `update-index.py` to update the index
3. Run `compile.py` to create updater script
4. Run `out/sync.bat` by double clicking the file
5. Enjoy!

## Index Fetching
With a little bit of tweaking in the `sync.py` file, you could make the index file downloadable from anywhere. That would make everything even easier.