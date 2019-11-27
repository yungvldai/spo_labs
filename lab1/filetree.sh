#! /bin/bash

TABS=""
CALL_FROM=$(pwd)
rm -f ./log.csv
printf "Filepath\tFilename\tExtension\tSize (bytes)\tPermissions\tCreation date\tModify date\tMIME-type\tDuration (A/V), sec\tImage size (I), pxl\n" >> log.csv

function print_files() {
	DIRNAME=$(pwd)
	echo "${TABS}$(basename "$DIRNAME")"
	SAVEIFS=$IFS
	IFS=$(echo -en "\n\b")
	for filename in $@
	do
		files_list=($@)
		file_pos=$(( ${#files_list[*]} - 1 ))
		last_file=${files_list[$file_pos]}
		if [[ $filename == "$last_file" ]]; then
			MARKER="╚═"
		else 
			MARKER="╠═"
		fi
		if [[ -d "$filename" ]]; then
			TABS+="║ "
			FILES_IN_DIR=$(ls "$filename")
			cd "$filename"
			print_files "$FILES_IN_DIR"
			cd ..
			TABS=${TABS::${#TABS}-2}
		fi
		if [[ -f "$filename" ]]; then
    			NAME=$(echo "$filename")
			EXTENSION=$(echo "$filename" | sed 's/^.*\.//')
			SIZE=$(wc -c "$filename" | awk '{print $1}')
			MIME=$(file -ib "$filename")
			PERM=$(stat -c "%A" "$filename")
			DATE_CREATED=$(stat -c "%w" "$filename" | awk '{print $1}')
			DATE_MODIFIED=$(stat -c "%y" "$filename" | awk '{print $1}')
			DUR="None"
			IMGWH="None"

			if file "$filename" | grep -qE 'image|bitmap'; then
				IMGWH=$(identify -format '%wx%h' "$filename")
			elif file -ib "$filename" | grep -qE 'video'; then
				DUR=$(ffprobe -i "$filename" -show_entries format=duration -v quiet -of csv="p=0")
			elif file -ib "$filename" | grep -qE 'audio'; then
				DUR=$(mp3info -p "%S\n" "$filename")
	 		fi
			echo "${TABS}""$MARKER $NAME, $SIZE bytes."

			BACK=$(pwd)			
			cd "$CALL_FROM"
			printf "%s" "$BACK\t$NAME\t$EXTENSION\t$SIZE\t$PERM\t$DATE_CREATED\t$DATE_MODIFIED\t$MIME\t$DUR\t$IMGWH\n" >> log.csv
			cd "$BACK"
		fi
	done
	IFS=$SAVEIFS
}

FILES=$(ls "$1")
cd "$1"
print_files "$FILES"
echo -e "\n"Done. Made with "❤️" by Vlad Ivanov.
