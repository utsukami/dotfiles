for x in $(xinput | grep G502 | cut -f 2 | grep -o '[0-9]*'); do
	$(xinput --set-prop $x 284 10)
done
