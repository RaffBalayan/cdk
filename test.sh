#!/bin/bash

dir="$1"
timestart=$(date +"%d.%m.%Y_%H.%M.%S")

paths=($(find $1 -type f))

for j in ${!paths[@]}; do
	size[$j]=$(ls -l ${paths[$j]} | awk '{print $5}')
	hash[$j]=$(cd /opt/itHash/;/opt/itHash/itFileControl --hash --file ${paths[$j]} --alg belt 2> /dev/null)
	file[$j]=${paths[$j]}
done

timeend=$(date +"%d.%m.%Y_%H.%M.%S")

printf "<?xml version=\"1.0\"?>\n"
printf "<root>\n"
printf "\t<time>\n"
	printf "\t\t<hashStart time=%s\n" "\"${timestart}\"/>"
	printf "\t\t<hashEnd time=%s\n" "\"${timestart}\"/>"
	printf "\t\t<checkStart time=%s\n" "\"${timeend}\"/>"
	printf "\t\t<checkEnd time=%s\n" "\"${timeend}\"/>"
printf "\t</time>\n"
printf "\t<content>\n"
for i in ${!file[@]}; do
	printf "<file hash=\"%s\" originalPath=\"%s\" size=\"%s\" status=\"ok\" algorithm=\"belt\"/>\n" "${hash[$i]}" "${file[$i]}" "${size[$i]}"
done
printf "\t</content>\n"
printf "</root>\n"
