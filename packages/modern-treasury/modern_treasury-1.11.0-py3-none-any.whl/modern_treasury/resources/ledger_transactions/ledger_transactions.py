# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from datetime import date, datetime
from typing_extensions import Literal

from ...types import (
    LedgerTransaction,
    ledger_transaction_list_params,
    ledger_transaction_create_params,
    ledger_transaction_update_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform
from .versions import Versions, AsyncVersions
from ..._resource import SyncAPIResource, AsyncAPIResource
from ...pagination import SyncPage, AsyncPage
from ..._base_client import AsyncPaginator, make_request_options

if TYPE_CHECKING:
    from ..._client import ModernTreasury, AsyncModernTreasury

__all__ = ["LedgerTransactions", "AsyncLedgerTransactions"]


class LedgerTransactions(SyncAPIResource):
    versions: Versions

    def __init__(self, client: ModernTreasury) -> None:
        super().__init__(client)
        self.versions = Versions(client)

    def create(
        self,
        *,
        effective_date: Union[str, date],
        ledger_entries: List[ledger_transaction_create_params.LedgerEntry],
        description: Optional[str] | NotGiven = NOT_GIVEN,
        external_id: str | NotGiven = NOT_GIVEN,
        ledgerable_id: str | NotGiven = NOT_GIVEN,
        ledgerable_type: Literal[
            "counterparty",
            "expected_payment",
            "incoming_payment_detail",
            "internal_account",
            "line_item",
            "paper_item",
            "payment_order",
            "payment_order_attempt",
            "return",
            "reversal",
        ]
        | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: Literal["archived", "pending", "posted"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        idempotency_key: str | None = None,
    ) -> LedgerTransaction:
        """
        Create a ledger transaction.

        Args:
          effective_date: The date (YYYY-MM-DD) on which the ledger transaction happened for reporting
              purposes.

          ledger_entries: An array of ledger entry objects.

          description: An optional description for internal use.

          external_id: A unique string to represent the ledger transaction. Only one pending or posted
              ledger transaction may have this ID in the ledger.

          ledgerable_id: If the ledger transaction can be reconciled to another object in Modern
              Treasury, the id will be populated here, otherwise null.

          ledgerable_type: If the ledger transaction can be reconciled to another object in Modern
              Treasury, the type will be populated here, otherwise null. This can be one of
              payment_order, incoming_payment_detail, expected_payment, return, or reversal.

          metadata: Additional data represented as key-value pairs. Both the key and value must be
              strings.

          status: To post a ledger transaction at creation, use `posted`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/api/ledger_transactions",
            body=maybe_transform(
                {
                    "description": description,
                    "status": status,
                    "metadata": metadata,
                    "effective_date": effective_date,
                    "ledger_entries": ledger_entries,
                    "external_id": external_id,
                    "ledgerable_type": ledgerable_type,
                    "ledgerable_id": ledgerable_id,
                },
                ledger_transaction_create_params.LedgerTransactionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                idempotency_key=idempotency_key,
            ),
            cast_to=LedgerTransaction,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
    ) -> LedgerTransaction:
        """Get details on a single ledger transaction."""
        return self._get(
            f"/api/ledger_transactions/{id}",
            options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body),
            cast_to=LedgerTransaction,
        )

    def update(
        self,
        id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        ledger_entries: List[ledger_transaction_update_params.LedgerEntry] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: Literal["archived", "pending", "posted"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        idempotency_key: str | None = None,
    ) -> LedgerTransaction:
        """
        Update the details of a ledger transaction.

        Args:
          description: An optional description for internal use.

          ledger_entries: An array of ledger entry objects.

          metadata: Additional data represented as key-value pairs. Both the key and value must be
              strings.

          status: To post a ledger transaction at creation, use `posted`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._patch(
            f"/api/ledger_transactions/{id}",
            body=maybe_transform(
                {
                    "description": description,
                    "status": status,
                    "metadata": metadata,
                    "ledger_entries": ledger_entries,
                },
                ledger_transaction_update_params.LedgerTransactionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                idempotency_key=idempotency_key,
            ),
            cast_to=LedgerTransaction,
        )

    def list(
        self,
        *,
        after_cursor: Optional[str] | NotGiven = NOT_GIVEN,
        effective_at: Dict[str, str] | NotGiven = NOT_GIVEN,
        effective_date: Dict[str, Union[str, datetime]] | NotGiven = NOT_GIVEN,
        external_id: str | NotGiven = NOT_GIVEN,
        ledger_account_category_id: str | NotGiven = NOT_GIVEN,
        ledger_account_id: str | NotGiven = NOT_GIVEN,
        ledger_id: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        order_by: ledger_transaction_list_params.OrderBy | NotGiven = NOT_GIVEN,
        per_page: int | NotGiven = NOT_GIVEN,
        posted_at: Dict[str, Union[str, datetime]] | NotGiven = NOT_GIVEN,
        status: Literal["pending", "posted", "archived"] | NotGiven = NOT_GIVEN,
        updated_at: Dict[str, Union[str, datetime]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
    ) -> SyncPage[LedgerTransaction]:
        """
        Get a list of ledger transactions.

        Args:
          effective_at: Use "gt" (>), "gte" (>=), "lt" (<), "lte" (<=), or "eq" (=) to filter by
              effective at. For example, for all transactions after Jan 1 2000, use
              effective_at%5Bgt%5D=2000-01-01T00:00:00:00.000Z.

          effective_date: Use `gt` (>), `gte` (>=), `lt` (<), `lte` (<=), or `eq` (=) to filter by
              effective date. For example, for all dates after Jan 1 2000, use
              effective_date%5Bgt%5D=2000-01-01.

          metadata: For example, if you want to query for records with metadata key `Type` and value
              `Loan`, the query would be `metadata%5BType%5D=Loan`. This encodes the query
              parameters.

          order_by: Order by `created_at` and/or `effective_at` in `asc` or `desc` order. For
              example, to order by `effective_at asc`, use `order_by%5Beffective_at%5D=asc`.
              Ordering by only one field at a time is supported.

          posted_at: Use `gt` (>), `gte` (>=), `lt` (<), `lte` (<=), or `eq` (=) to filter by the
              posted at timestamp. For example, for all times after Jan 1 2000 12:00 UTC, use
              posted_at%5Bgt%5D=2000-01-01T12:00:00Z.

          updated_at: Use `gt` (>), `gte` (>=), `lt` (<), `lte` (<=), or `eq` (=) to filter by the
              posted at timestamp. For example, for all times after Jan 1 2000 12:00 UTC, use
              updated_at%5Bgt%5D=2000-01-01T12:00:00Z.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request
        """
        return self._get_api_list(
            "/api/ledger_transactions",
            page=SyncPage[LedgerTransaction],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                query=maybe_transform(
                    {
                        "after_cursor": after_cursor,
                        "per_page": per_page,
                        "metadata": metadata,
                        "ledger_id": ledger_id,
                        "ledger_account_id": ledger_account_id,
                        "effective_at": effective_at,
                        "effective_date": effective_date,
                        "posted_at": posted_at,
                        "updated_at": updated_at,
                        "order_by": order_by,
                        "status": status,
                        "external_id": external_id,
                        "ledger_account_category_id": ledger_account_category_id,
                    },
                    ledger_transaction_list_params.LedgerTransactionListParams,
                ),
            ),
            model=LedgerTransaction,
        )


class AsyncLedgerTransactions(AsyncAPIResource):
    versions: AsyncVersions

    def __init__(self, client: AsyncModernTreasury) -> None:
        super().__init__(client)
        self.versions = AsyncVersions(client)

    async def create(
        self,
        *,
        effective_date: Union[str, date],
        ledger_entries: List[ledger_transaction_create_params.LedgerEntry],
        description: Optional[str] | NotGiven = NOT_GIVEN,
        external_id: str | NotGiven = NOT_GIVEN,
        ledgerable_id: str | NotGiven = NOT_GIVEN,
        ledgerable_type: Literal[
            "counterparty",
            "expected_payment",
            "incoming_payment_detail",
            "internal_account",
            "line_item",
            "paper_item",
            "payment_order",
            "payment_order_attempt",
            "return",
            "reversal",
        ]
        | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: Literal["archived", "pending", "posted"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        idempotency_key: str | None = None,
    ) -> LedgerTransaction:
        """
        Create a ledger transaction.

        Args:
          effective_date: The date (YYYY-MM-DD) on which the ledger transaction happened for reporting
              purposes.

          ledger_entries: An array of ledger entry objects.

          description: An optional description for internal use.

          external_id: A unique string to represent the ledger transaction. Only one pending or posted
              ledger transaction may have this ID in the ledger.

          ledgerable_id: If the ledger transaction can be reconciled to another object in Modern
              Treasury, the id will be populated here, otherwise null.

          ledgerable_type: If the ledger transaction can be reconciled to another object in Modern
              Treasury, the type will be populated here, otherwise null. This can be one of
              payment_order, incoming_payment_detail, expected_payment, return, or reversal.

          metadata: Additional data represented as key-value pairs. Both the key and value must be
              strings.

          status: To post a ledger transaction at creation, use `posted`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/api/ledger_transactions",
            body=maybe_transform(
                {
                    "description": description,
                    "status": status,
                    "metadata": metadata,
                    "effective_date": effective_date,
                    "ledger_entries": ledger_entries,
                    "external_id": external_id,
                    "ledgerable_type": ledgerable_type,
                    "ledgerable_id": ledgerable_id,
                },
                ledger_transaction_create_params.LedgerTransactionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                idempotency_key=idempotency_key,
            ),
            cast_to=LedgerTransaction,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
    ) -> LedgerTransaction:
        """Get details on a single ledger transaction."""
        return await self._get(
            f"/api/ledger_transactions/{id}",
            options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body),
            cast_to=LedgerTransaction,
        )

    async def update(
        self,
        id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        ledger_entries: List[ledger_transaction_update_params.LedgerEntry] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        status: Literal["archived", "pending", "posted"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        idempotency_key: str | None = None,
    ) -> LedgerTransaction:
        """
        Update the details of a ledger transaction.

        Args:
          description: An optional description for internal use.

          ledger_entries: An array of ledger entry objects.

          metadata: Additional data represented as key-value pairs. Both the key and value must be
              strings.

          status: To post a ledger transaction at creation, use `posted`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._patch(
            f"/api/ledger_transactions/{id}",
            body=maybe_transform(
                {
                    "description": description,
                    "status": status,
                    "metadata": metadata,
                    "ledger_entries": ledger_entries,
                },
                ledger_transaction_update_params.LedgerTransactionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                idempotency_key=idempotency_key,
            ),
            cast_to=LedgerTransaction,
        )

    def list(
        self,
        *,
        after_cursor: Optional[str] | NotGiven = NOT_GIVEN,
        effective_at: Dict[str, str] | NotGiven = NOT_GIVEN,
        effective_date: Dict[str, Union[str, datetime]] | NotGiven = NOT_GIVEN,
        external_id: str | NotGiven = NOT_GIVEN,
        ledger_account_category_id: str | NotGiven = NOT_GIVEN,
        ledger_account_id: str | NotGiven = NOT_GIVEN,
        ledger_id: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        order_by: ledger_transaction_list_params.OrderBy | NotGiven = NOT_GIVEN,
        per_page: int | NotGiven = NOT_GIVEN,
        posted_at: Dict[str, Union[str, datetime]] | NotGiven = NOT_GIVEN,
        status: Literal["pending", "posted", "archived"] | NotGiven = NOT_GIVEN,
        updated_at: Dict[str, Union[str, datetime]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
    ) -> AsyncPaginator[LedgerTransaction, AsyncPage[LedgerTransaction]]:
        """
        Get a list of ledger transactions.

        Args:
          effective_at: Use "gt" (>), "gte" (>=), "lt" (<), "lte" (<=), or "eq" (=) to filter by
              effective at. For example, for all transactions after Jan 1 2000, use
              effective_at%5Bgt%5D=2000-01-01T00:00:00:00.000Z.

          effective_date: Use `gt` (>), `gte` (>=), `lt` (<), `lte` (<=), or `eq` (=) to filter by
              effective date. For example, for all dates after Jan 1 2000, use
              effective_date%5Bgt%5D=2000-01-01.

          metadata: For example, if you want to query for records with metadata key `Type` and value
              `Loan`, the query would be `metadata%5BType%5D=Loan`. This encodes the query
              parameters.

          order_by: Order by `created_at` and/or `effective_at` in `asc` or `desc` order. For
              example, to order by `effective_at asc`, use `order_by%5Beffective_at%5D=asc`.
              Ordering by only one field at a time is supported.

          posted_at: Use `gt` (>), `gte` (>=), `lt` (<), `lte` (<=), or `eq` (=) to filter by the
              posted at timestamp. For example, for all times after Jan 1 2000 12:00 UTC, use
              posted_at%5Bgt%5D=2000-01-01T12:00:00Z.

          updated_at: Use `gt` (>), `gte` (>=), `lt` (<), `lte` (<=), or `eq` (=) to filter by the
              posted at timestamp. For example, for all times after Jan 1 2000 12:00 UTC, use
              updated_at%5Bgt%5D=2000-01-01T12:00:00Z.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request
        """
        return self._get_api_list(
            "/api/ledger_transactions",
            page=AsyncPage[LedgerTransaction],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                query=maybe_transform(
                    {
                        "after_cursor": after_cursor,
                        "per_page": per_page,
                        "metadata": metadata,
                        "ledger_id": ledger_id,
                        "ledger_account_id": ledger_account_id,
                        "effective_at": effective_at,
                        "effective_date": effective_date,
                        "posted_at": posted_at,
                        "updated_at": updated_at,
                        "order_by": order_by,
                        "status": status,
                        "external_id": external_id,
                        "ledger_account_category_id": ledger_account_category_id,
                    },
                    ledger_transaction_list_params.LedgerTransactionListParams,
                ),
            ),
            model=LedgerTransaction,
        )
