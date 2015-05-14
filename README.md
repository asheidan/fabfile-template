# fabfile-template

A template fabfile for turn-key deployment

## Why?

Why should you use this? Deploying Python projects to a web server is quite straight-forward, but external dependencies and database migrations quickly makes deployment tedious and error-prone since it's easy to forget a step or two.

The initial goal of this project is to automate the common deployment process used where I work. Perhaps I will, if I can be bothered, extend the functionality to also include more general deployment scenarios.

## Deploy

Currently the only implemented transfer-method is pushing to a bare git repository located on the server and then using `git-export --format=tar | tar xf -` to write a given commit to a new directory.

The default setup uses a separate directory for each new deploy (named releases). This is to prevent old byte-compiled files to linger and also makes it easy to do rollbacks.

