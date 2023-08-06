# 功能

Tkinter小游戏框架

# 用法

像Example那样，写一个类继承Game，再实现一些必要的方法，即可做出一个完整的小游戏。

# 启动Example

```python
from tkinter_game import Game, Example

Example()
```

# 注意事项

画界面之前，Canvas需要清空画布，不然会造成内存泄漏。

```python
delete("all")
```