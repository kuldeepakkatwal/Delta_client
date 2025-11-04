# Documentation

Complete documentation for the Delta Exchange Python Client.

---

## 📚 Documentation Structure

This directory contains all detailed documentation for the Delta Exchange Python Client library.

---

## 📖 Available Guides

### **[Options Trading Guide](options-guide.md)** 📊
Complete guide to trading options on Delta Exchange.
- Options basics (calls vs puts, long vs short)
- Symbol format and contract discovery
- Trading strategies (spreads, straddles, iron condors)
- Risk management and position sizing
- Real-time monitoring with WebSocket

**Start here if you want to trade options!**

---

### **[WebSocket Guide](websocket-guide.md)** 🔌
Complete guide to real-time data streaming.
- Connection management and authentication
- Public channels (ticker, orderbook, trades)
- Private channels (orders, positions, fills)
- Reconnection handling
- Advanced patterns and best practices

**Start here if you want real-time market data!**

---

### **[Architecture](architecture.md)** 🔧
Technical specification and design documentation.
- Project architecture and components
- Development roadmap and phases
- Implementation details
- API design decisions

**For understanding the internals and contributing.**

---

### **[Testing Guide](testing.md)** 🧪
Complete guide to testing the client.
- How to test REST API
- How to test WebSocket
- How to test options trading
- Troubleshooting and debugging
- Test results and validation

**For ensuring everything works correctly.**

---

## 🚀 Quick Start

New to the library? Follow this path:

1. **Installation** - See [main README](../README.md)
2. **Basic Usage** - See [main README](../README.md)
3. **Code Examples** - See [examples/](../examples/)
4. **Options Trading** - See [options-guide.md](options-guide.md)
5. **Real-Time Data** - See [websocket-guide.md](websocket-guide.md)
6. **Testing** - See [testing.md](testing.md)

---

## 📂 Repository Structure

```
delta-exchange-python/
├── README.md              ← Start here (main documentation)
├── docs/                  ← You are here (detailed guides)
│   ├── options-guide.md
│   ├── websocket-guide.md
│   ├── architecture.md
│   └── testing.md
├── examples/              ← Working code examples
├── tests/                 ← Test scripts
└── delta_exchange/        ← Source code
```

---

## 🎯 By Use Case

### I want to trade futures
→ See [main README](../README.md) and [examples/place_order.py](../examples/place_order.py)

### I want to trade options
→ See **[options-guide.md](options-guide.md)**

### I want real-time data
→ See **[websocket-guide.md](websocket-guide.md)**

### I want to test the client
→ See **[testing.md](testing.md)**

### I want to understand the architecture
→ See **[architecture.md](architecture.md)**

---

## 💡 Additional Resources

- **Main README**: [../README.md](../README.md)
- **Code Examples**: [../examples/](../examples/)
- **Test Scripts**: [../tests/](../tests/)
- **Source Code**: [../delta_exchange/](../delta_exchange/)

---

## 🤝 Contributing

See [architecture.md](architecture.md) for:
- Project structure
- Design decisions
- Development phases
- How to contribute

---

**All documentation is included in this repository. No external hosting required!**

