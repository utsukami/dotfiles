for x in $(xinput | grep G502 | cut -f 2 | grep -o '[0-9]*'); do
		$(xinput --set-prop $x $(xinput --list-props $x | cut -f 2 | grep -o 'Con.\{1,25\}' | grep -o '[0-9]*') 8)
		$(xinput --set-prop $x $(xinput --list-props $x | cut -f 2 | grep -o 'Ada.\{1,25\}' | grep -o '[0-9]*') 8)
done
