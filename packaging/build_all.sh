# May need to adjust these to fit your installation
MSBUILD='/cygdrive/c/Windows/Microsoft.NET/Framework/v3.5/MSBuild.exe'
export PATH=$PATH:/cygdrive/c/Program\ Files/Windows\ Installer\ XML\ v3/bin
CANDLE="candle.exe"
LIGHT="light.exe"
TEMP_WXS_DIR="wxstemp"

function run_or_exit {
    echo "Running command '$1'"
    eval $1
    if [ $? != 0 ]; then
        exit
    fi
}

function usage {
    echo "USAGE: build_project VERSION"
    echo
    echo "Version MUST be in this format: (MAJ).(MIN).(BUILD)"
}

BUILD_VERSION=$1
MAJ=`echo $BUILD_VERSION | awk -F'.' '{print $1}'`
MIN=`echo $BUILD_VERSION | awk -F'.' '{print $2}'`
BUILD=`echo $BUILD_VERSION | awk -F'.' '{print $3}'`

if [ "$MAJ" == "" ]; then
    usage
    exit 1
fi
if [ "$MIN" == "" ]; then
    usage
    exit 1
fi
if [ "$BUILD" == "" ]; then
    usage
    exit 1
fi
echo "The packages will be built at version $BUILD_VERSION ($MAJ, $MIN, $BUILD)"
echo "Is this what you want to do (yes or no)?"
read q
if [ "$q" != "yes" ]; then
  echo "Aborting and doing nothing."
  exit 1
fi
echo ""

echo "Cleaning project"
pushd ..
make clean
echo "Building project"
make PROJECTVERSION=$BUILD_VERSION
popd
echo "Cleaning packaging directory"
make clean
echo "Creating version file"
PRODUCTCODE="{`uuidgen.exe|dos2unix|tr a-z A-Z`}"
PRODUCTVER="$MAJ.$MIN.$BUILD"
echo "Building MSI files"

# set the version info
BASE_WIX_FILE="Example"
PRODUCT_NAME="Example"
OUTPUT_WIX_FILE="$BASE_WIX_FILE-$PRODUCTVER"

echo "Versioning $PRODUCT_NAME with version number $PRODUCTVER and product code $PRODUCTCODE (output file: $OUTPUT_WIX_FILE.wxs)"
if [ ! -d $TEMP_WXS_DIR ]; then
    mkdir $TEMP_WXS_DIR;
fi
sed "s/SEARCHANDREPLACEPRODUCTCODE/$PRODUCTCODE/g; s/SEARCHANDREPLACEPRODUCTVERSION/$PRODUCTVER/g" $BASE_WIX_FILE.wxs > $TEMP_WXS_DIR/$OUTPUT_WIX_FILE.wxs

# build the package
run_or_exit "$CANDLE -out $TEMP_WXS_DIR/$OUTPUT_WIX_FILE.wixobj $TEMP_WXS_DIR/$OUTPUT_WIX_FILE.wxs"
run_or_exit "$LIGHT -out $OUTPUT_WIX_FILE.msi -ext WixUIExtension -ext WixUtilExtension $TEMP_WXS_DIR/$OUTPUT_WIX_FILE.wixobj"

# If you have a code signing certificate, you can fill in the details to sign the package
# run_or_exit "signtool.exe sign /f YourPrivateKey.pfx /p YourKeyPassword /t http://timestamp.comodoca.com/authenticode /d \"$PRODUCT_NAME Installer\" /v $OUTPUT_WIX_FILE.msi"
