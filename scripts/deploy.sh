git submodule update --init --recursive
git submodule update --remote --merge
cd hexo && hexo clean && hexo generate && hexo deploy
