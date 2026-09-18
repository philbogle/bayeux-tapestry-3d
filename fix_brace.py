import sys

with open('index.html', 'r') as f:
    content = f.read()

brace_old = """                        loading: false,
                        failed: false
                    });
                }
            }

        // Scene background and fog for depth (dark earthy tone)"""

brace_new = """                        loading: false,
                        failed: false
                    });
                }
            }
        } // end !isPhone

        // Scene background and fog for depth (dark earthy tone)"""

content = content.replace(brace_old, brace_new)

with open('index.html', 'w') as f:
    f.write(content)
