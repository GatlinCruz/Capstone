class Host:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def __str__(self):
        return self.name + ": ip - " + self.ip

    def __repr__(self):
        return self.name + ": ip - " + self.ip

    def add_to_file(self):
        return self.name + " = net.addHost( '" + self.name + "' )\n"


class Switch:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def add_to_file(self):
        return self.name + " = net.addSwitch( '" + self.name + "' )\n"


class Controller:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def add_to_file(self):
        return self.name + " = net.addController( '" + self.name + "' )\n"


class Link:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return self.first + " <-> " + self.second

    def __repr__(self):
        return self.first + " <-> " + self.second

    def add_to_file(self):
        return self.first + self.second + " = net.addLink( '" + self.first + "', " + "'" + self.second + "' )\n"


graph = {
    "hosts": [],
    "switches": [],
    "controllers": [],
    "links": []
}

if __name__ == '__main__':

    h1 = Host("h1", "127.0.0.1")
    print(h1)

    s1 = Switch("s1")
    print(s1)

    c1 = Controller("c1")
    print(c1)

    l1 = Link(h1, s1)
    print(l1)

    graph['hosts'].append(h1)
    graph['switches'].append(s1)
    graph['controllers'].append(c1)
    graph['links'].append(l1)

    print(graph)  # uses __repr__ for printing
    print(graph.get('hosts')[0])  # uses __str__ for printing
