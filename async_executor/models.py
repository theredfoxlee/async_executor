from .utils import md5

import rom
import time


class User(rom.Model):
    name = rom.String(required=True, unique=True)
    password_h = rom.String(required=True)

    @classmethod
    def create(cls, name, password):
        password_h = md5(password)
        return cls(name=name.encode(), password_h=password_h.encode())

    @classmethod
    def get_by(cls, name):
        return super(User, cls).get_by(name=name.encode())

    def compare(self, password):
        password_h = md5(password)
        print(f'{password_h} == {self.password_h.decode()}')
        return self.password_h.decode() == password_h

    def json(self):
        return {
            'name': self.name.decode(),
            'password_h': self.password_h.decode()
        }


class Task(rom.Model):
    name = rom.String(required=True, unique=True)
    args = rom.String(required=True)
    status = rom.String(required=True)
    returncode = rom.String()
    stdout = rom.String()
    stderr = rom.String()
    reporter = rom.ManyToOne(
        'User', on_delete='cascade', required=True)
    created_at = rom.Float(required=True, default=time.time)
    duration = rom.Float()

    @classmethod
    def create(cls, name, args, reporter):
        return cls(
            name=name.encode(),
            args=args.encode(),
            status=b'CREATED',
            reporter=reporter
        )

    @classmethod
    def get_by(cls, name):
        return super(Task, cls).get_by(name=name.encode())

    @classmethod
    def get_by2(cls, reporter):
        return super(Task, cls).get_by(reporter=reporter)

    def update_done(self, returncode, stdout, stderr, duration):
        self.status = b'DONE'
        self.returncode = str(returncode).encode()
        self.stdout = stdout.encode() if type(stdout) == str else stdout
        self.stderr = stderr.encode() if type(stderr) == str else stderr
        self.duration = duration
        self.save()

    def json(self):
        return {
            'name': self.name.decode(),
            'args': self.args.decode(),
            'status': self.status.decode(),
            'returncode': (self.returncode.decode()
                           if self.returncode is not None
                           else self.returncode),
            'stdout': (self.stdout.decode().splitlines()
                       if self.stdout is not None
                       else self.stdout),
            'stderr': (self.stderr.decode().splitlines()
                       if self.stderr is not None
                       else self.stderr),
            'reporter': self.reporter.name.decode(),
            'created_at': self.created_at,
            'duration': self.duration
        }
