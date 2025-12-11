# 🐚 Nature Shell

> **A revolutionary shell scripting language based on parts of speech**  
> Designed and built by a 13-year-old developer

---

## 🌟 What makes Nature Shell special?

- **Natural Language Syntax**: Commands read like sentences
- **Type Safety**: Explicit type annotations prevent errors
- **Intuitive Design**: Based on linguistic parts of speech
- **Beginner Friendly**: Easy to learn, powerful to use

## 🚀 Quick Start

### Installation
```bash
# Coming soon
pip install nature-shell
```

### Your First Script
```bash
# Create a variable
var:int crt $count -in 0

# Loop and print
$count < 5 -while {
    tmp echo "Count: $count"
    var ch $count -in $count + 1
}
```

### Try It Now
```bash
python main.py
>>> var:str crt $name -in "World"
>>> tmp echo "Hello, $name"
Hello, World
```

## 💡 Why Nature Shell?

### Traditional Bash
```bash
if [ $usage -gt 80 ]; then
    echo "Out of memory"
else
    echo "Normal"
fi
```

### Nature Shell
```bash
$usage > 80 -if {
    echo "Out of memory"
} -else {
    echo "Normal"
}
```

**More readable. More intuitive. More natural.**

## 📖 The Story Behind Nature Shell

I'm a 13-year-old middle school student who got frustrated with traditional shell syntax. 

**The problem:** Bash, PowerShell, and other shells felt unintuitive and hard to remember.

**The solution:** What if commands followed natural language structure? What if we used parts of speech (nouns, verbs, adjectives) as a foundation?

That's how Nature Shell was born.

### Design Philosophy
- **Readability over brevity**: Code should read like sentences
- **Consistency over convention**: Everything follows the same rules
- **Safety over flexibility**: Types prevent silent errors

This is my first major project. I'm learning as I go, and I'd love your feedback! ⭐

## 🚧 Current Status

**This is a work in progress!** 

### ✅ Implemented
- [x] Variables (create, modify, retrieve)
- [x] Basic I/O (echo)
- [x] System commands
- [x] Error handling
- [x] REPL interface

### 🔨 In Progress
- [ ] Conditionals (-if, -else)
- [ ] Loops (-foreach, -while)
- [ ] Pipelines (|)
- [ ] Functions (fn def)
- [ ] Type checking

### 💭 Planned
- [ ] Standard library
- [ ] Package manager
- [ ] VSCode extension
- [ ] Documentation site

## 📚 Documentation

## 🎬 Demo

## 🤝 Contributing

## 📄 License

## 💬 Contact
