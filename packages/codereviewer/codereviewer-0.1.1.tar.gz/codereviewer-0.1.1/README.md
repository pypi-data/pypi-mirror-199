# codereviewer
Multiplatform program to help programmers in fast code reviews with quality.

    Usage:
        python3 codereviewer
            [--version| -v          ] The current version (Version 0.1.0).
            [--help   | -h          ] This help. Each option also has its own help.
            [--dir    | -d <path>   ] A path to a directory to be analyzed by codereviewer.
            [--file   | -f <path>   ] A path to a file to be analyzed by codereviewer.
            [--option | -op <option>] <fix|review|fix-review> whether you want to review-only, fix-only or both.
            [--require| -rq <file>  ] A json file containing rules for not allowed sentences and/or regular expressions.
            [--refuse | -rf <file>  ] A json file containing rules for allowed sentences and/or regular expressions.
            [--out    | -o <file>   ] A file containing the lines of code to be changed with the violations highlighted.
    
    Examples:
        Check examples/codereviewer_require.json and examples/codereviewer_refuse.json 
