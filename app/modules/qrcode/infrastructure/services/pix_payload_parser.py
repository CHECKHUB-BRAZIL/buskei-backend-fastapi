from app.modules.qrcode.domain.value_objects.pix_payload_data import (
    PixPayloadData,
)


class PixPayloadParser:
    """
    Parser básico para payload PIX EMV.
    """

    def parse(
        self,
        payload: str,
    ) -> PixPayloadData:

        fields = self._parse_emv(
            payload,
        )

        merchant_name = fields.get("59")

        city = fields.get("60")

        amount = self._parse_amount(
            fields.get("54")
        )

        pix_key = self._extract_pix_key(
            fields.get("26")
        )

        txid = self._extract_txid(
            fields.get("62")
        )

        is_valid_crc = (
            self._validate_crc(payload)
        )

        return PixPayloadData(
            pix_key=pix_key,
            merchant_name=merchant_name,
            city=city,
            amount=amount,
            txid=txid,
            is_valid_crc=is_valid_crc,
        )

    def _parse_emv(
        self,
        payload: str,
    ) -> dict[str, str]:

        result = {}

        index = 0

        while index + 4 <= len(payload):

            tag = payload[index:index + 2]

            length_str = payload[
                index + 2:index + 4
            ]

            if not length_str.isdigit():
                break

            length = int(length_str)

            value_start = index + 4

            value_end = (
                value_start + length
            )

            if value_end > len(payload):
                break

            value = payload[
                value_start:value_end
            ]

            result[tag] = value

            index = value_end

        return result

    def _extract_pix_key(
        self,
        merchant_info: str | None,
    ) -> str | None:

        if not merchant_info:
            return None

        inner = self._parse_emv(
            merchant_info
        )

        return inner.get("01")

    def _extract_txid(
        self,
        additional_data: str | None,
    ) -> str | None:

        if not additional_data:
            return None

        inner = self._parse_emv(
            additional_data
        )

        return inner.get("05")

    def _parse_amount(
        self,
        amount: str | None,
    ) -> float | None:

        if not amount:
            return None

        try:
            return float(amount)

        except ValueError:
            return None

    def _validate_crc(
        self,
        payload: str,
    ) -> bool:

        if "6304" not in payload:
            return False

        crc_index = payload.rfind(
            "6304"
        )

        received_crc = payload[
            crc_index + 4:
            crc_index + 8
        ]

        payload_for_crc = payload[
            :crc_index + 4
        ]

        calculated_crc = (
            self._calculate_crc16(
                payload_for_crc
            )
        )

        return (
            received_crc.upper()
            == calculated_crc.upper()
        )

    def _calculate_crc16(
        self,
        payload: str,
    ) -> str:

        polynomial = 0x1021

        crc = 0xFFFF

        data = payload.encode(
            "utf-8"
        )

        for byte in data:

            crc ^= byte << 8

            for _ in range(8):

                if crc & 0x8000:
                    crc = (
                        (crc << 1)
                        ^ polynomial
                    )

                else:
                    crc <<= 1

                crc &= 0xFFFF

        return (
            hex(crc)
            .replace("0x", "")
            .upper()
            .zfill(4)
        )
