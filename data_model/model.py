class User(object):
    def __init__(self, user_id, name, password_hash, email_address, is_admin):
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash
        self.email_address = email_address
        self.is_admin = is_admin

    def get_user_attributes(self):
        return {'user_id': self.user_id, 'name': self.name, 'password_hash': self.password_hash,
                'email_address': self.email_address, 'is_admin': self.is_admin}


class UserRepository:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.user_id] = user

    def remove_user(self, user_id):
        self.users.pop(user_id, None)

    def get_user_by_id(self, user_id):
        try:
            return self.users[user_id]
        except KeyError:
            print("User {} not found".format(user_id))


class House(User):
    def __init__(self, user_id, house_id, name):
        self.user_id = user_id
        self.house_id = house_id
        self.name = name

    def get_house_attributes(self):
        return {'user_id': self.user_id, 'house_id': self.house_id, 'name': self.name}


# House groups are for users with multiple houses, or for Fleet management
class HouseRepository:
    def __init__(self):
        self.houses = {}

    def add_house(self, house):
        self.houses[house.house_id] = house

    def remove_house(self, house_id):
        self.houses.pop(house_id, None)

    def get_house_by_id(self, house_id):
        try:
            return self.houses[house_id]
        except KeyError:
            print("House %d not found" % house_id)

    def add_house_to_user(self, user, house):
        house.user_id = user.id

    def get_houses_for_user(self, user_id):
        lst = []
        for house in self.houses:
            if house.user_id == user_id:
                lst += house
        return lst


class HouseGroup(object):
    def __init__(self, house_id):
        self.house_id = house_id

    def get_house_group_attributes(self):
        return {'house_id': self.house_id}


class HouseGroupRepository:
    def __init__(self):
        self.house_groups = {}

    def add_house_group(self, house_group):
        self.house_groups[house_group.id] = house_group

    def add_house_to_group(self, house_group):
        self.house_groups[house_group.id] += self.house_groups

    def remove_house_group(self, house_group_id):
        self.house_groups.pop(house_group_id, None)


class Room(House):
    def __init__(self, house_id, room_id, name):
        self.house_id = house_id
        self.room_id = room_id
        self.name = name

    def get_room_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id, 'name': self.name}


# Room groups could be things like 'Upstairs', or to be used for templates
class RoomRepository:
    def __init__(self):
        self.rooms = {}

    #    self.room_groups = {}

    def add_room(self, room):
        self.rooms[room.id] = room

    # def add_room_group(self, room_group):
    #    self.room_groups[room_group.id] = room_group

    # def add_room_to_group(self, room, room_group):
    #    self.room_groups[room_group.id] = []
    #    self.room_groups[room_group.id] += self.rooms[room.id]

    def remove_room(self, room_id):
        self.rooms.pop(room_id, None)

    def get_room_by_id(self, room_id):
        try:
            return self.rooms[room_id]
        except KeyError:
            print("Room %d not found" % room_id)

    def get_devices_for_room(self, devices, room_id):
        lst = []
        for device in devices:
            if device.room_id == room_id:
                lst += device
        return lst

    def add_room_to_house(self, house, room_id):
        house += self.rooms[room_id]

    def get_rooms_for_house(self, rooms, house_id):
        lst = []
        for room in rooms:
            if room.house_id == house_id:
                lst += room
        return lst


class Device(House, Room):
    def __init__(self, house_id, room_id, device_id, name, device_type, power_state, last_temp, target_temp,
                 sensor_data):
        self.house_id = house_id
        self.room_id = room_id
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.power_state = power_state
        self.last_temp = last_temp
        self.target_temp = target_temp
        self.sensor_data = sensor_data

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id, 'device_id': self.device_id, 'name': self.name,
                'type': self.type, 'power_state': self.power_state, 'last_temp': self.last_temp,
                'target_temp': self.target_temp, 'sensor_data': self.sensor_data}

    def change_power_state(self):
        try:
            if self.power_state == 1:
                self.power_state = 0
            elif self.power_state == 0:
                self.power_state = 1
        except:
            return "ERROR: Power State not 1 or 0"

    def set_target_temp(self, target):
        self.target_temp = target



# class Thermostat(Device):
#     def __init__(self, house_id, room_id, device_id, name, power_state, last_temp, target_temp):
#         super(Device, self).__init__(house_id, room_id, device_id, name, power_state)
#         self.last_temp = last_temp
#         self.target_temp = target_temp


class DeviceRepository:
    def __init__(self):
        self.devices = {}

    def add_device(self, device):
        self.devices[device.id] = device

    def remove_device(self, device_id):
        self.devices.pop(device_id, None)

    def get_device_by_id(self, device_id):
        try:
            return self.devices[device_id]
        except KeyError:
            print("Device %d not found" % device_id)

    def add_device_to_house(self, house, device_id):
        house += self.devices[device_id]

    def get_devices_for_house(self, devices, house_id):
        lst = []
        for device in devices:
            if device.house_id == house_id:
                lst += device
        return lst

    def add_device_to_room(self, room, device_id):
        room += self.devices[device_id]

    def get_devices_for_room(self, devices, room_id):
        lst = []
        for device in devices:
            if device.room_id == room_id:
                lst += device
        return lst


class DeviceGroups(object):
    def __init__(self, device_id, device_group_id):
        self.device_id = device_id
        self.device_group_id = device_group_id

    def get_device_group_attributes(self):
        return {'device_id': self.device_id, 'device_group_id': self.device_group_id}


class DeviceGroupRepository:
    def __init__(self):
        self.device_groups = {}

    def add_device_group(self, device_group):
        self.device_groups[device_group.id] = device_group

    def add_device_to_group(self, device_id, device_group):
        self.device_groups[device_group.id] += device_id

    def remove_device_group(self, device_group_id):
        self.device_groups.pop(device_group_id.id, None)

    def get_device_group_by_id(self, device_group_id):
        try:
            return self.device_groups[device_group_id]
        except KeyError:
            print("Device Group {} not found" % device_group_id)
