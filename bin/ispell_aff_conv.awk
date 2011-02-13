BEGIN { ruls_found = 0; FS="[>#]"; }

/^#/	  { print $0; next; }
/^[[:space:]]*$/	  { print $0; if( ruls_found) { ruls_found = 0; } next; }

/^flag */ { split($0, arr, " "); flag = arr[2]; gsub("[*:]", "", flag); print "SFX " flag " Y " 100000; FS="[>#]";}

/.*>.*/	  { 
	    ruls_found = 1;
/*    print $1 " @ " $2 " @ " $3;  */
/*    print $0; */
	    suff = tolower($1);
	    gsub( "[[:space:]]", "", suff );
	    tocut_newend = tolower($2);
	    gsub( "[[:space:]]", "", tocut_newend );

	    if( index(tocut_newend, "-") == 0 ) {
		tocut = "0";
		newend = tocut_newend;
	    }
	    else 
	    if( index(tocut_newend, ",") == 0 ) {
		tocut = substr(tocut_newend, 2);
		newend = "0";
	    }
	    else {
		split(tocut_newend, arr, ",");
		tocut = substr(arr[1], 2);
		newend = arr[2];
	    }

	    if( index(tocut, "-") == 1 ) tocut = sub(tocut, 2);
	    
	    print "SFX " flag "   " tocut "\t" newend "\t" suff "\t\t#" $3 $4 $5 $6;

	    }

END {}
