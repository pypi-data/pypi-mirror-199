# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import os
os.environ['PYTHON_SETTINGS_MODULE'] = __name__

from cbra.ext.sendgrid import SendgridEmailSender


EMAIL_SERVER: str = 'sendgrid'

EMAIL_CREDENTIAL: str = os.environ['SENDGRID_API_KEY']


async def main():
    sender = SendgridEmailSender()
    await sender.send_template(
        sender="Noek de Feber <noreply@suppliers.molanohq.com>",
        recipients=["cochise.ruhulessin@unimatrixone.io"],
        subject="Please confirm order by Molano",
        context={
            'access_code': '123456',
            'heading': "Please confirm our order",
            'purchase_order_url': 'https://suppliers.molanohq.com/orders/1'
        },
        template='accept-purchase-order.html.j2',
    )


if __name__ == '__main__':
    asyncio.run(main())