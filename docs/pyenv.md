# Pyenv

## python

```sh
git clone https://github.com/pyenv/pyenv.git $HOME/.zen/opt/pyenv

# python
export PYENV_ROOT="$HOME/.zen/opt/pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

pyenv install 3.7.3
pyenv global 3.7.3
```

## ruby

```sh
git clone https://github.com/rbenv/rbenv.git $HOME/.zen/opt/rbenv

# ruby
export RBENV_ROOT="$HOME/.zen/opt/rbenv"
export PATH=${RBENV_ROOT}/bin:$PATH
eval "$(rbenv init -)"

mkdir -p "$(rbenv root)"/plugins
git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-doctor | bash

rbenv install 2.6.6
rbenv global 2.6.6
```
