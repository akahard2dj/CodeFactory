- git 에서 https repository 연결시 SSL 인증서 오류 해결법


```bash
$ git config --global http.sslVerify false
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
