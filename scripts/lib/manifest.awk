# Deliberately limited manifest grammar: one flat JSON object with scalar values.
# Never evaluate input. Preserve raw unknown scalar fields; reject richer JSON.
function bad() { failed=1; exit 1 }
function ws() { while (substr(text,pos,1) ~ /^[ \t\r\n]$/) pos++ }
function string_token(    start,c,e,i) {
    start=pos
    if (substr(text,pos++,1) != "\"") bad()
    while (pos <= length(text)) {
        c=substr(text,pos++,1)
        if (c == "\"") return substr(text,start,pos-start)
        if (c ~ /[[:cntrl:]]/) bad()
        if (c == "\\") {
            e=substr(text,pos++,1)
            if (e == "u") {
                for (i=0;i<4;i++) if (substr(text,pos++,1) !~ /^[0-9a-fA-F]$/) bad()
            } else if (e !~ /^["\\\/bfnrt]$/) bad()
        }
    }
    bad()
}
{ text=text $0 "\n" }
END {
    if (failed) exit 1
    pos=1; ws()
    if (substr(text,pos++,1) != "{") bad()
    ws()
    while (substr(text,pos,1) != "}") {
        key=string_token()
        # Plain ASCII keys make duplicate detection unambiguous (no escaped aliases).
        if (key !~ /^"[A-Za-z_][A-Za-z0-9_]*"$/ || seen[key]++) bad()
        ws(); if (substr(text,pos++,1) != ":") bad(); ws()
        if (substr(text,pos,1) == "\"") value=string_token()
        else {
            start=pos
            while (pos<=length(text) && substr(text,pos,1) !~ /[ ,}\t\r\n]/) pos++
            value=substr(text,start,pos-start)
            if (value !~ /^(true|false|null|-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?)$/) bad()
        }
        values[key]=value
        if (key != "\"foundation_version\"") entries[++count]=key ": " value
        ws(); c=substr(text,pos++,1)
        if (c=="}") { pos--; break }
        if (c!=",") bad()
        ws(); if (substr(text,pos,1)=="}") bad()
    }
    pos++; ws(); if (pos<=length(text)) bad()
    if (values["\"foundation\""] != "\"digital-factory-ai-agents\"" ||
        values["\"agent\""] != "\"backend\"" || values["\"stack\""] != "\"laravel\"" ||
        values["\"security_agent\""] != "true" || values["\"audit_agent\""] != "true") bad()
    if (mode=="legacy") { if (seen["\"foundation_version\""]) print "yes"; exit }
    print "{"
    for (i=1;i<=count;i++) printf "  %s%s\n", entries[i], (i<count ? "," : "")
    print "}"
}
