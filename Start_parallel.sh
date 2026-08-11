# add data management
if [ -z "$1" ]
then
    echo "Give the number of CPUs!!!"
    exit
else
    #echo "\$var is NOT empty"
    cpun=$1
fi

if [ -z "$2" ]
then
    #echo "\$var is empty"
    dn='tmp_'$(date +%s)
else
    #echo "\$var is NOT empty"
    dn=$2'_'$(date +%s)
fi

# Force git commit
# python git_force_commit.py

echo $dn > last_run
mkdir -p $dn/scripts
cp -r *.hoc *.py mod_files $dn/scripts
echo '**' > $dn/.gitignore
# Store git commit tag
git log --decorate > $dn/scripts/git.log

cd $dn/scripts
nrnivmodl mod_files
time mpiexec -n $cpun nrniv -mpi run_parallel.py 2>&1 | tee run.log 
python pull_data_branch.py 2>&1 | tee -a run.log 
mv store_multi_pulled.hdf5 ..
cd ../..