Userside module for python
==========================

Install
-------

You can install userside module via pip

     pip install pyuserside
     


Examples
--------

Sync API
~~~~~~~~~

.. code:: python

    from pyuserside.api.synchronous import UsersideAPI

    usapi = UsersideAPI(url='https://localhost/api.php', key='my_secret_key')

    device_id = usapi.device.get_device_id(object_type='switch',
                                           data_typer='ip',
                                           data_value='10.90.90.90')
    devices = uapi.device.get_data(object_type='switch', object_id=device_id)
    target_device = devices[str(device_id)]

Or context manager:

.. code:: python

    from pyuserside.api.synchronous import UsersideAPI

    with UsersideAPI(url='https://localhost/api.php', key='my_secret_key') as uapi:
        device_id = usapi.device.get_device_id(object_type='switch',
                                               data_typer='ip',
                                               data_value='10.90.90.90')
        devices = uapi.device.get_data(object_type='switch', object_id=device_id)
        target_device = devices[str(device_id)]

Async API
~~~~~~~~~

Same here

.. code:: python

    from pyuserside.api.asynchronous import UsersideAPI
    import asyncio

    async def main():
        usapi = UsersideAPI(url='https://localhost/api.php', key='my_secret_key')

        device_id = await usapi.device.get_device_id(object_type='switch',
                                                     data_typer='ip',
                                                     data_value='10.90.90.90')
        devices = await usapi.device.get_data(object_type='switch', object_id=device_id)
        target_device = devices[str(device_id)]

    asyncio.run(main())

Or async context manager:

.. code:: python

    from pyuserside.api.asynchronous import UsersideAPI
    import asyncio

    async def main():
        async with UsersideAPI(url='https://localhost/api.php', key='my_secret_key') as usapi:
            device_id = await usapi.device.get_device_id(object_type='switch',
                                                         data_typer='ip',
                                                         data_value='10.90.90.90')
            devices = await usapi.device.get_data(object_type='switch', object_id=device_id)
            target_device = devices[str(device_id)]
    
    asyncio.run(main())