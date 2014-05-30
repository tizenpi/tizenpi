#!/bin/bash

# do wygnerowania  zrobionych
#cat ~/rpmList.txt | grep Zrobione | sed 's/ --.*//' > speclist

# do poprawienia listy
#while read name; do if [ ! -e "$name.spec" ]; then echo "brak $name"; fi; done < speclist

num=$(wc -l speclist | tr -dc '0-9')
cur=0

while read name; do
    cur=$[cur+1]
    echo "$cur/$num: $name"
    rpmbuild -ba --nodeps --target=armv6l-tizen_softfp "$name.spec" &> "rebuild_$name.log";
    if [ $? -ne 0 ]; then
        echo -e "    \033[30m\033[41m FAILED \033[m"
    fi
done < speclist
