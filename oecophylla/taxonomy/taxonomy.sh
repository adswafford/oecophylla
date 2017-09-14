conda env create --name shotgun-metaphlan2 -f shotgun-metaphlan2.yaml
conda env create --name shotgun-kraken -f shotgun-kraken.yaml

# currently shogun is a hack, running the install script until we
# have stable conda install
conda env create --name shotgun-shogun -f shotgun-shogun.yaml

source activate shotgun-shogun

echo $CONDA_PREFIX

mkdir -p $CONDA_PREFIX/etc/conda/activate.d
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d

touch $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
touch $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

echo "#!/bin/sh" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo "export OLD_PATH=$PATH" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo "export PATH=$PATH:$PWD/utree" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh


echo "#!/bin/sh" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
echo "export PATH=$OLD_PATH" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
echo "unset OLDPATH" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh


# download UTree binary and add to path
if hash wget 2>/dev/null; then
    wget https://github.com/knights-lab/UTree/releases/download/v1.2/utree_1.2_linux.zip
else
    curl -L -o utree_1.2_linux.zip https://github.com/knights-lab/UTree/releases/download/v1.2/utree_1.2_linux.zip
fi
unzip utree_1.2_linux.zip -d utree
chmod 755 utree/utree*
