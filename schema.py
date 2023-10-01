schema_register = {"type": "object",
                   "minProperties": 2,
                   "maxProperties": 2,
                   "properties": {
                       "username": {"type": "string"},
                       "password": {"type": "string"},
                   }, "required": ["username", "password"]
                   }
