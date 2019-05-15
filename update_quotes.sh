SCRIPT_DIR=$( cd $(dirname $0) ; pwd -P )

# Update quotes only from Monday to Friday
if [[ $(date +%u) -lt 6 ]] ; then
    python3 ${SCRIPT_DIR}/update_quotes.py
fi
