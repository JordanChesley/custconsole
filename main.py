import custconsole

cc = custconsole.custconsole(name="CLI Demo", version="1.0.0")


@cc.command(name='juice', description='Box of juice')
def hi(person):
    print(f'Hello {person}!')


cc.run()
