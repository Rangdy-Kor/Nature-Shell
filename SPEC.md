# Nature Shell

# Features

- Pipeline usage
- Concise yet intuitive object-based syntax
- Object-based output

## Single Command Structure

(Permission) (Noun)(:Adjective) (Verb) (-Adverb) (Value) (-Preposition) (Value)

## Command Chaining (Conjunction)

(Condition1) (-Conjunction) (Condition2) ... (-Control Statement)

# Parts of Speech

## Comment

Not a part of speech, but comments can be marked by starting with //, ##, or cmt.

## Permission

Specifies the highest execution permission for the command. If omitted, it runs with user (normal) permission.

## Noun

Specifies the target object on which the command acts.

## Adjective

Defines detailed attributes of the noun. Starts with : and is placed immediately after the noun.

## Verb

Specifies the action the noun object will perform.

## Adverb

Modifies how the verb is executed. Starts with a hyphen (-) and follows immediately after the verb.

## Value

The actual data required by the command. Arithmetic expressions are permitted within the value section.

### Arithmetic Expressions

- +: Addition
- -: Subtraction
- *: Multiplication
- /: Division
- %: Modulus (remainder)
- **: Exponentiation

### Special Variables

- $_ : Value passed from the pipeline or the current item in a loop
### Variable Rules

- Variables always start with $.
- Can use letters, numbers, underscores (_), and hyphens (-).
- Cannot start with a number.
- Valid examples: $count, $user_name, $file-path

## Prepositions

Connect values to define their relationship. Begins with a hyphen (-).

## Conjunctions

Logically connect conditional expressions or commands. Begins with a hyphen (-), but unlike prepositions, it is followed by another conditional expression or command, not a value object.

# Function List

## Permissions

- root: Full system control permission.
- admin: Administrator permission.
- user: General user permission. Default when permission is omitted.

## Nouns

- file/fl: File object
- directory/dir: Directory path object
- folder/fd: Folder object
- variable/var: Script variable
- system/sys: System and environment settings
- function/func/fn: Function object
- module/mod: Module object
- tmp: Temporary object
- application/aplc/app: App object
- network/net: Network object

## Adjectives

Data Types
- byte/byt
- short/sht
- int
- long/lng
- float/flo
- double/dou
- char/chr
- string/str
- bool
- array/arr
- list/ls
- tuple/tup
- map
- set
File Extensions
- txt
- doc
- docx
- ppt
- pptx
- xls
- xlsx
- png
- jpeg/jpe/jpg
- gif
- bmp
- heic
- raw
- mp3
- wav
- m4a
- mp4
- mov
- mkv
- json
- xml
- yaml
- csv
Network
- url
- ip
- port
Filtering
- running/run
- stopped/stp
- size
- memory/mem
- service/svc
## Verbs

General Verbs
- change/chg/ch: Change
- remove/rmv/rm: Remove
- create/crt: Create
- list/ls: Return list
- start/strt: Start
- stop/stp: Stop
- restart/rest: Restart
- echo: Output object
- cast: Cast type
- get: Get value
- sort: Sort
- convert/conv: convert
- def: define function
- return/ret: return value
- read/rd: read data
- write/wrt: write/overwrite data
- append/apnd: append data
Comparison Verbs
- >: greater than
- >=: greater than or equal to
- <: less than
- <=: less than or equal to
- ==: equal to
- !=: not equal

## Adverbs

- -force/-frc: force execution
- -question/-qst: prompt for confirmation before execution
- -recurse/-rcs: recursive function
- -delay/-dly: wait before execution
- -asce: ascending order
- -desc: descending order

## Prepositions

- -if {}: if
- -else {}: else
- -foreach {}/-for {}: repeat for each
- -while {}/whl {}: repeat while
- -catch {}/-cat {}: catch exception/error
- -connect/-conc {}: connect to external system
- -until/-unt {}: wait until a specific condition
- -to: to
- -in: in
- -of: of (possessive)
- -quality/-qual: quality

## Conjunctions

- -and/-a: and (logical AND)
- -or/-o: or (logical OR)
- -not/-n: negation (logical negation)

### Priority

1. -not (highest priority)
2. -and
3. -or (lowest priority)

Explicit priority can be specified using parentheses ()

Example: ($cpu > 80 -and $mem > 80) -or $emergency_mode

## Example

## Variable Creation

```

var:int crt $age -in 25
var:str crt $name -in “John”
var:list crt $items -in [1, 2, 3]
```

## File Operations

```
dir ch C:/path
file crt test.txt -in “Hello, World!”
file:txt ls -rcs C:/home/user
root fd rm -frc c:/path
```

## Conditional Execution

```
sys:mem get | var:int crt $usage -in $_
$usage > 80 -if {
    echo “Out of memory”
} -else {
    echo “Normal”
}
```

## Loops

```
file:txt ls | -foreach {
    echo “File: $_ ”
}

var:int crt $i -in 0
$i < 10 -while {
    echo $i
    var ch $i -in $i + 1
}
```

## Pipeline Chaining

```
file:log ls |
    file:size sort -desc |
    var:list crt $top5 -in $_ |
    echo $_
```

## System Manipulation

```
root sys stop -qst -dly 5s
```

## Practical Examples

### Backup Script

```
sys:date get -format “%Y%m%d” | var:str crt $today -in $_
file:log ls -rcs /var/logs |
    -foreach {
        file copy $_ -to /backup/$today/$_
     }
```

### System Monitoring

```
sys:cpu get | var:int crt $cpu -in $_
sys:mem get | var:int crt $mem -in $_

$cpu > 80 -and $mem > 80 -if {
     echo “System Overloaded!”
	 sys:serv rest high-usage-app
} -else {
    echo “System normal”
}
```

### Delete Temporary Files Older Than 30 Days

```
file:tmp ls /temp |
    file:age > 30d -if {
        file rm -frc $_
    }
```

### Batch image conversion

```
file:jpg ls /photos |
    -foreach {
        file conv $_ -to png -qual 90
        echo “Conversion complete: $_ ”
    }
```

### Function definition and usage

```
fn def create-backup-dir ($format) {
    sys:date get -format $format | var:str crt $date-path -in $_
    dir crt /backup/$date-path -cat {
        tmp echo “Error: Could not create backup directory.”
        ret false
    }
    ret /backup/$date-path
}

create-backup-dir “%Y%m%d” | var:str crt $today-dir -in $_

$today-dir != false -if {
    echo “Backup directory created successfully: $today-dir”
} -else {
    echo “Script terminated: Backup failed. ”
}
```

Translated with DeepL.com (free version)
