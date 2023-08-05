# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from canonical import StringType


class PolicyPrincipal(StringType):
    """Identifies a member (principal) in an access control list or
    role membership. A :class:`PolicyPrincipal` may be one of the following
    types:

    - `domain` - a specific domain. Domain membership is established by
      proving control over an email address for the domain.
    - `user` - a specific user, identified by email address.
    """
    __module__: str = 'cbra.types'
    principal_types: set[str] = {
        'domain'
        'user',
    }

    @classmethod
    def validate(cls, v: str) -> str:
        v = super().validate(v)
        t, _ = str.split(v, ':', 1)
        if t not in cls.principal_types:
            raise ValueError(f'invalid principal type: {t}')
        return cls(v)