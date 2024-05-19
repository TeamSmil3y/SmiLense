from pigeon import Pigeon
import settings

Pigeon(settings)

import views

from pigeon.conf import Manager

Pigeon.autorun = True
Pigeon.run(auto=True)
