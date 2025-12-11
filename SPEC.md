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

# Example



DeepL로 번역함 (https://dee.pl/apps)
