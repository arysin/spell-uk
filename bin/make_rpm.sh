#!/bin/sh

BUILDRPM_DIR="$HOME/rpmbuild"
RPM_BASENAME="$1"
VERSION="$2"

if [ "$RPM_BASENAME" = "" ] || [ "$VERSION" = "" ]; then
    echo "usage: $0 <rpmbasename> <version>"
    exit 1
fi

#rm -r $BUILDRPM_DIR
mkdir -p $BUILDRPM_DIR/SOURCES
mkdir -p $BUILDRPM_DIR/SPECS

SRC_PACKAGE="spell-uk-$VERSION.tgz"


if [ "$RPM_BASENAME" != "myspell-uk" ]; then

RPMNAME=$RPM_BASENAME-$VERSION
echo "Making $RPMNAME..."

cp dist/$SRC_PACKAGE /tmp
cp pkg/$RPM_BASENAME.spec /tmp

else

RPMNAME=${RPM_BASENAME}_UA-$VERSION
echo "Making $RPMNAME..."

cp dist/$SRC_PACKAGE /tmp
cp pkg/${RPM_BASENAME}.spec /tmp

fi

#su -c 
#mv /tmp/$SRC_PACKAGE $BUILDRPM_DIR/SOURCES; \
#	mv /tmp/$RPM_BASENAME.spec $BUILDRPM_DIR/SPECS; \
#	chown root.root $BUILDRPM_DIR/SOURCES/$SRC_PACKAGE $BUILDRPM_DIR/SPECS/$RPM_BASENAME.spec
#	cd $BUILDRPM_DIR/SPECS; \
#	rpmbuild -bs $RPM_BASENAME.spec

BASE_DIR=`pwd`

mv /tmp/$SRC_PACKAGE $BUILDRPM_DIR/SOURCES; \
	mv /tmp/$RPM_BASENAME.spec $BUILDRPM_DIR/SPECS; \
	cd $BUILDRPM_DIR/SPECS; \
	rpmbuild --buildroot $BUILDRPM_DIR -bs $RPM_BASENAME.spec

cd $BASE_DIR
mv $BUILDRPM_DIR/SRPMS/*spell*$VERSION*.src.rpm dist/
