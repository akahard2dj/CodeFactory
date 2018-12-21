- git 에서 https repository 연결시 SSL 인증서 오류 해결법


```bash
$ git config --global http.sslVerify false
```

- Configuring a remote for a fork
```bash
$ git remote -v
origin https://github.com/YOUR_USERNAME/YOUR_FORK.git (fetch)
origin https://github.com/YOUR_USERNAME/YOUR_FORK.git (push)

$ git remote add upstream hppts://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git

$ git remote -v
origin   https://github.com/YOUR_USERNAME/YOUR_FORK.git (fetch)
origin   https://github.com/YOUR_USERNAME/YOUR_FORK.git (push)
upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git (fetch)
upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git (push)

```


- Syncing a fork
```bash
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```


- Contributing code
1. Fork the project repository
2. clone sources from the project repository to my local disk:
```bash
$ git clone git@github.com:MyLogin/project.git
$ git remote add upstream https://github.com/project/project.git
```
3. create a branch to hold my changes:
```bash
$ git checkout -b my-feature
```
and start making changes. NEVER WORK IN THE MASTER BRANCH.

4. work on my computer, using Git to do the version control:
```bash
$ git add modified_files
$ git commit
```
to record my changes in Git, then push them to Github with:
```bash
$ git push -u origin my-feature
```
