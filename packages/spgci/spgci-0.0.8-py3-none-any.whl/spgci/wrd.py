from __future__ import annotations
from typing import Union, Optional
from requests import Response
from pandas import Series, DataFrame, to_datetime, json_normalize  # type: ignore
from spgci.api_client import get_data, Paginator
from spgci.utilities import odata_list_to_filter
from urllib.parse import urlencode, quote, parse_qs, urlparse
from datetime import date
from enum import Enum


class WorldRefineryData:
    """
    World Refinery Data.

    Includes
    --------
    ``RefTypes`` to use with the ``get_reference_data`` method.
    ``get_reference_data()`` to get the list of countries, owners, refineries, etc.. used in the World Refinery Database.
    ``get_capacity()`` to get refinery capacity changes.
    ``get_runs()`` to get annual crude runs for individual refineries.
    ``get_yields()`` to get the yields for individual refineries.
    ``get_outages()`` to get refinery outages.
    ``get_ownership()`` to get refinery ownership.
    ``get_margins()`` to get margin data.
    """

    _endpoint = "odata/refinery-data/v2/"

    class RefTypes(Enum):
        """World Refinery Database Reference Data Type"""

        CapacityStatuses = "CapacityStatuses"
        Cities = "cities"
        Configurations = "configurations"
        Countries = "countries"
        MarginTypes = "marginTypes"
        Operators = "operators"
        OutageUnits = "outageUnits"
        Owners = "owners"
        PADDs = "PADDs"
        # ProcessUnitCategories = "ProcessUnitCategories"
        ProcessUnits = "ProcessUnits"
        Refineries = "Refineries"
        Regions = "Regions"
        States = "States"

    @staticmethod
    def _padd_to_df(resp: Response) -> DataFrame:
        j = resp.json()
        df = json_normalize(
            j["value"],
            meta=["Id", "Name"],
            record_path="States",
            record_prefix="State.",
        )

        return df

    @staticmethod
    def _to_df(resp: Response) -> DataFrame:
        j = resp.json()
        df = json_normalize(j["value"])

        # duplicates due to $expand=*
        dupes = ["RefineryId", "OwnerId", "CapacityStatusId", "MarginTypeId"]
        df = df[df.columns.drop(dupes, "ignore")]  # type: ignore

        if len(df) > 0 and "ModifiedDate" in df.columns:
            df["ModifiedDate"] = to_datetime(df["ModifiedDate"], utc=True)  # type: ignore
        if len(df) > 0 and "Date" in df.columns:
            df["Date"] = to_datetime(df["Date"], utc=True)  # type: ignore

        return df

    @staticmethod
    def _paginate(resp: Response) -> Paginator:
        j = resp.json()

        count: int = j["@odata.count"]
        page_size = parse_qs(urlparse(resp.url).query)["pageSize"]

        if not page_size:
            return Paginator(False, "$skip", 0)

        remainder = count % int(page_size[0])
        quotient = count // int(page_size[0])
        total_pages = quotient + (1 if remainder > 0 else 0)

        if total_pages <= 1:
            return Paginator(False, "$skip", total_pages)

        return Paginator(True, "$skip", total_pages, pg_type="odata")

    def get_capacity(
        self,
        *,
        year: Optional[Union[int, list[int], "Series[int]"]] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        quarter: Optional[Union[int, list[int], "Series[int]"]] = None,
        refinery_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        owner: Optional[Union[str, list[str], "Series[str]"]] = None,
        capacity_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        capacity_status_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        process_unit: Optional[Union[str, list[str], "Series[str]"]] = None,
        filter_exp: Optional[str] = None,
        skip: int = 0,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        """
        Fetch historical refinery capacity changes.

        Parameters
        ----------
        year : Optional[Union[int, list[int], Series[int]]], optional
            filter by ``year = x``, by default None
        year_gt : Optional[int], optional
            filter by ``year > x``, by default None
        year_gte : Optional[int], optional
            filter by ``year >= x``, by default None
        year_lt : Optional[int], optional
            filter by ``year < x``, by default None
        year_lte : Optional[int], optional
            filter by ``year <= x``, by default None
        quarter : Optional[Union[int, list[int], Series[int]]], optional
            filter by quarter, by default None
        refinery_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by refineryId, by default None
        owner : Optional[Union[str, list[str], Series[str]]], optional
            filter by Owner/Name, by default None
        capacity_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by capacityId, by default None
        capacity_status_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by capacityStatusId, by default None
        process_unit : Optional[Union[str, list[str], Series[str]]], optional
            filter by ProcessUnit/Name, by default None
        filter_exp : Optional[str], optional
            pass-thru ``$filter`` query param to use a handcrafted filter expression, by default None
        skip : int, optional
            pass-thru ``$skip`` query param to skip a certain number of records, by default 0
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default False
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
              DataFrame of the ``response.json()``
            Response
              Raw ``requests.Response`` object
        Examples
        --------
        **Simple**
        >>> WorldRefineryData().get_capacity(year=2008)

        **Using Lists**
        >>> WorldRefineryData().get_capacity(year_gte=2022, process_unit=["Atmos Distillation", "Dist Hydrocracking"])

        **Using Series**
        >>> df = WorldRefineryData().get_reference_data(type=WorldRefineryData.RefTypes.Refineries)
        >>> WorldRefineryData().get_capacity(year=2020, refinery_id=df["Id"][:3])
        """
        endpoint = "capacity"

        filter_params: list[str] = []

        filter_params.append(odata_list_to_filter("Year", year))
        filter_params.append(odata_list_to_filter("Quarter", quarter))
        filter_params.append(odata_list_to_filter("RefineryId", refinery_id))
        filter_params.append(odata_list_to_filter("Owner/Name", owner))
        filter_params.append(odata_list_to_filter("CapacityId", capacity_id))
        filter_params.append(
            odata_list_to_filter("CapacityStatusId", capacity_status_id)
        )
        filter_params.append(odata_list_to_filter("ProcessUnit/Name", process_unit))

        if year_gt:
            filter_params.append(f"year gt {year_gt}")
        if year_gte:
            filter_params.append(f"year ge {year_gte}")
        if year_lt:
            filter_params.append(f"year lt {year_lt}")
        if year_lte:
            filter_params.append(f"year le {year_lte}")

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        else:
            filter_exp += " AND " + " AND ".join(filter_params)

        params = {
            "$skip": skip,
            "pageSize": page_size,
            "$count": "true",
            "$expand": "*",
        }

        if filter_exp:
            params["$filter"] = filter_exp

        # odata endpoint will not allow '+' character in URL seemingly
        qs = urlencode(params, quote_via=quote)

        return get_data(
            path=f"{self._endpoint}{endpoint}?{qs}",
            params={},
            # params=params,
            paginate=paginate,
            raw=raw,
            df_fn=self._to_df,
            paginate_fn=self._paginate,
        )

    def get_runs(
        self,
        *,
        year: Optional[Union[int, list[int], "Series[int]"]] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        quarter: Optional[Union[int, list[int], "Series[int]"]] = None,
        refinery_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        owner: Optional[Union[str, list[str], "Series[int]"]] = None,
        capacity_status_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        process_unit: Optional[Union[str, list[str], "Series[str]"]] = None,
        filter_exp: Optional[str] = None,
        skip: int = 0,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        """
        Fetch annual crude runs by refinery.

        Parameters
        ----------
        year : Optional[Union[int, list[int], Series[int]]], optional
            filter by ``year = x``, by default None
        year_gt : Optional[int], optional
            filter by ``year > x``, by default None
        year_gte : Optional[int], optional
            filter by ``year >= x``, by default None
        year_lt : Optional[int], optional
            filter by ``year < x``, by default None
        year_lte : Optional[int], optional
            filter by ``year <= x``, by default None
        quarter : Optional[Union[int, list[int], Series[int]]], optional
            filter by quarter, by default None
        refinery_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by refineryId, by default None
        owner : Optional[Union[str, list[str], Series[str]]], optional
            filter by Owner/Name, by default None
        capacity_status_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by CapacityStatusId, by default None
        process_unit : Optional[Union[str, list[str], Series[str]]], optional
            filter by ProcessUnit/Name, by default None
        filter_exp : Optional[str], optional
            pass-thru ``$filter`` query param to use a handcrafted filter expression, by default None
        skip : int, optional
            pass-thru ``$skip`` query param to skip a certain number of records, by default 0
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default False
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
              DataFrame of the ``response.json()``
            Response
              Raw ``requests.Response`` object
        Examples
        --------
        **Simple**
        >>> WorldRefineryData().get_runs(owner="BP")

        **Using Lists**
        >>> WorldRefineryData().get_runs(year_gte=2020, refinery_id=[18, 357])

        **Using Series**
        >>> df = WorldRefineryData().get_reference_data(type=WorldRefineryData.RefTypes.ProcessUnits)
        >>> WorldRefineryData().get_runs(year=2020, process_unit=df["Name"][:-10], refineryId=1)
        """
        endpoint = "runs"

        filter_params: list[str] = []

        filter_params.append(odata_list_to_filter("Year", year))
        filter_params.append(odata_list_to_filter("Quarter", quarter))
        filter_params.append(odata_list_to_filter("RefineryId", refinery_id))
        filter_params.append(odata_list_to_filter("Owner/Name", owner))
        filter_params.append(
            odata_list_to_filter("CapacityStatusId", capacity_status_id)
        )
        filter_params.append(odata_list_to_filter("ProcessUnit/Name", process_unit))

        if year_gt:
            filter_params.append(f"year gt {year_gt}")
        if year_gte:
            filter_params.append(f"year ge {year_gte}")
        if year_lt:
            filter_params.append(f"year lt {year_lt}")
        if year_lte:
            filter_params.append(f"year le {year_lte}")

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        else:
            filter_exp += " AND " + " AND ".join(filter_params)

        params = {
            "$skip": skip,
            "pageSize": page_size,
            "$count": "true",
            "$expand": "*",
        }

        if filter_exp:
            params["$filter"] = filter_exp

        # odata endpoint will not allow '+' character in URL seemingly
        qs = urlencode(params, quote_via=quote)

        return get_data(
            path=f"{self._endpoint}{endpoint}?{qs}",
            params={},
            # params=params,
            paginate=paginate,
            raw=raw,
            df_fn=self._to_df,
            paginate_fn=self._paginate,
        )

    def get_yields(
        self,
        *,
        year: Optional[Union[int, list[int], "Series[int]"]] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        quarter: Optional[Union[int, list[int], "Series[int]"]] = None,
        refinery_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        owner: Optional[Union[str, list[str], "Series[str]"]] = None,
        capacity_status_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        process_unit: Optional[Union[str, list[str], "Series[str]"]] = None,
        filter_exp: Optional[str] = None,
        skip: int = 0,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        """
        Fetch refinery yields by year.

        Parameters
        ----------
        year : Optional[Union[int, list[int], Series[int]]], optional
            filter by ``year = x``, by default None
        year_gt : Optional[int], optional
            filter by ``year > x``, by default None
        year_gte : Optional[int], optional
            filter by ``year >= x``, by default None
        year_lt : Optional[int], optional
            filter by ``year < x``, by default None
        year_lte : Optional[int], optional
            filter by ``year <= x``, by default None
        quarter : Optional[Union[int, list[int], Series[int]]], optional
            filter by quarter, by default None
        refinery_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by refineryId, by default None
        owner : Optional[Union[str, list[str], Series[str]]], optional
            filter by Owner/Name, by default None
        capacity_status_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by CapacityStatusId, by default None
        process_unit : Optional[Union[str, list[str], Series[str]]], optional
            filter by ProcessUnit/Name, by default None
        filter_exp : Optional[str], optional
            pass-thru ``$filter`` query param to use a handcrafted filter expression, by default None
        skip : int, optional
            pass-thru ``$skip`` query param to skip a certain number of records, by default 0
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default False
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
              DataFrame of the ``response.json()``
            Response
              Raw ``requests.Response`` object
        Examples
        --------
        **Simple**
        >>> WorldRefineryData().get_yields(refineryId=1)

        **Using Lists**
        >>> WorldRefineryData().get_yields(year=2020, owner=["BP", "S N Repal"])

        **Using Series**
        >>> df = WorldRefineryData().get_reference_data(type=WorldRefineryData.RefTypes.ProcessUnits)
        >>> WorldRefineryData().get_yields(year=2020, process_unit=df["Name"][:-10], refineryId=1)
        """
        endpoint = "runs"

        filter_params: list[str] = []

        filter_params.append(odata_list_to_filter("Year", year))
        filter_params.append(odata_list_to_filter("Quarter", quarter))
        filter_params.append(odata_list_to_filter("RefineryId", refinery_id))
        filter_params.append(odata_list_to_filter("Owner/Name", owner))
        filter_params.append(
            odata_list_to_filter("CapacityStatusId", capacity_status_id)
        )
        filter_params.append(odata_list_to_filter("ProcessUnit/Name", process_unit))

        if year_gt:
            filter_params.append(f"year gt {year_gt}")
        if year_gte:
            filter_params.append(f"year ge {year_gte}")
        if year_lt:
            filter_params.append(f"year lt {year_lt}")
        if year_lte:
            filter_params.append(f"year le {year_lte}")

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        else:
            filter_exp += " AND " + " AND ".join(filter_params)

        params = {
            "$skip": skip,
            "pageSize": page_size,
            "$count": "true",
            "$expand": "*",
        }

        if filter_exp:
            params["$filter"] = filter_exp

        # odata endpoint will not allow '+' character in URL seemingly
        qs = urlencode(params, quote_via=quote)

        return get_data(
            path=f"{self._endpoint}{endpoint}?{qs}",
            params={},
            # params=params,
            paginate=paginate,
            raw=raw,
            df_fn=self._to_df,
            paginate_fn=self._paginate,
        )

    def get_outages(
        self,
        *,
        year: Optional[Union[int, list[int], "Series[int]"]] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        date: Optional[Union[date, list[date], "Series[date]"]] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        quarter: Optional[Union[int, list[int], "Series[int]"]] = None,
        refinery_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        owner: Optional[Union[str, list[str], "Series[str]"]] = None,
        process_unit: Optional[Union[str, list[str], "Series[str]"]] = None,
        planning_status: Optional[Union[str, list[str], "Series[str]"]] = None,
        outage_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        outage_vol: Optional[Union[float, list[float], "Series[float]"]] = None,
        outage_vol_gt: Optional[float] = None,
        outage_vol_gte: Optional[float] = None,
        outage_vol_lt: Optional[float] = None,
        outage_vol_lte: Optional[float] = None,
        filter_exp: Optional[str] = None,
        skip: int = 0,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        """
        Fetch refinery outages.

        Parameters
        ----------
        year : Optional[Union[int, list[int], Series[int]]], optional
            filter by ``year = x`` , by default None
        year_gt : Optional[int], optional
            filter by ``year > x`` , by default None
        year_gte : Optional[int], optional
            filter by ``year >= x`` , by default None
        year_lt : Optional[int], optional
            filter by ``year < x`` , by default None
        year_lte : Optional[int], optional
            filter by ``year <= x`` , by default None
        date : Optional[Union[date, list[date], Series[date]]], optional
            filter by ``date = x`` , by default None
        date_gt : Optional[date], optional
            filter by ``date > x`` , by default None
        date_gte : Optional[date], optional
            filter by ``date >= x`` , by default None
        date_lt : Optional[date], optional
            filter by ``date < x`` , by default None
        date_lte : Optional[date], optional
            filter by ``date <= x`` , by default None
        quarter : Optional[Union[int, list[int], Series[int]]], optional
            filter by quarter, by default None
        refinery_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by refineryId, by default None
        owner : Optional[Union[str, list[str], Series[str]]], optional
            filter by Owner/Name, by default None
        process_unit : Optional[Union[str, list[str], Series[str]]], optional
            filter by ProcessUnit/Name, by default None
        planning_status : Optional[Union[str, list[str], Series[str]]], optional
            filter by PlanningStatus, by default None
        outage_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by outageId, by default None
        outage_vol : Optional[Union[float, list[float], Series[float]]], optional
            filter by ``OutageVol_MBD = x`` , by default None
        outage_vol_gt : Optional[float], optional
            filter by ``OutageVol_MBD > x`` , by default None
        outage_vol_gte : Optional[float], optional
            filter by ``OutageVol_MBD >= x`` , by default None
        outage_vol_lt : Optional[float], optional
            filter by ``OutageVol_MBD < x`` , by default None
        outage_vol_lte : Optional[float], optional
            filter by ``OutageVol_MBD <= x`` , by default None
        filter_exp : Optional[str], optional
            pass-thru ``$filter`` query param to use a handcrafted filter expression, by default None
        skip : int, optional
            pass-thru ``$skip`` query param to skip a certain number of records, by default 0
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default False
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
              DataFrame of the ``response.json()``
            Response
              Raw ``requests.Response`` object
        Examples
        --------
        **Simple**
        >>> WorldRefineryData().get_outages(year=2020, quarter=3)

        **Using Lists**
        >>> WorldRefineryData().get_outages(year=2020, planning_status="Unplanned", process_unit=["Coker", "CDU"])

        **Using Series**
        >>> df = WorldRefineryData().get_reference_data(type=WorldRefineryData.RefTypes.Refineries)
        >>> df = df[df['Country.Name'] == "Mexico"]
        >>> WorldRefineryData().get_outages(outage_vol_gte=200, refinery_id=df['Id'])
        """
        endpoint = "outages"

        filter_params: list[str] = []

        filter_params.append(odata_list_to_filter("Year", year))
        filter_params.append(odata_list_to_filter("Date", date))
        filter_params.append(odata_list_to_filter("OutageVol_MBD", outage_vol))
        filter_params.append(odata_list_to_filter("Quarter", quarter))
        filter_params.append(odata_list_to_filter("RefineryId", refinery_id))
        filter_params.append(odata_list_to_filter("Owner/Name", owner))
        filter_params.append(odata_list_to_filter("ProcessUnit/Name", process_unit))
        filter_params.append(odata_list_to_filter("PlanningStatus", planning_status))
        filter_params.append(odata_list_to_filter("OutageId", outage_id))

        if year_gt:
            filter_params.append(f"year gt {year_gt}")
        if year_gte:
            filter_params.append(f"year ge {year_gte}")
        if year_lt:
            filter_params.append(f"year lt {year_lt}")
        if year_lte:
            filter_params.append(f"year le {year_lte}")

        if date_gt:
            filter_params.append(f"Date gt {date_gt}")
        if date_gte:
            filter_params.append(f"Date ge {date_gte}")
        if date_lt:
            filter_params.append(f"Date lt {date_lt}")
        if date_lte:
            filter_params.append(f"Date le {date_lte}")

        if outage_vol_gt:
            filter_params.append(f"OutageVol_MBD gt {outage_vol_gt}")
        if outage_vol_gte:
            filter_params.append(f"OutageVol_MBD ge {outage_vol_gte}")
        if outage_vol_lt:
            filter_params.append(f"OutageVol_MBD lt {outage_vol_lt}")
        if outage_vol_lte:
            filter_params.append(f"OutageVol_MBD le {outage_vol_lte}")

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        else:
            filter_exp += " AND " + " AND ".join(filter_params)

        params = {
            "$skip": skip,
            "pageSize": page_size,
            "$count": "true",
            "$expand": "*",
        }

        if filter_exp:
            params["$filter"] = filter_exp

        # odata endpoint will not allow '+' character in URL seemingly
        qs = urlencode(params, quote_via=quote)

        return get_data(
            path=f"{self._endpoint}{endpoint}?{qs}",
            params={},
            # params=params,
            paginate=paginate,
            raw=raw,
            df_fn=self._to_df,
            paginate_fn=self._paginate,
        )

    def get_ownership(
        self,
        *,
        year: Optional[Union[int, list[int], "Series[int]"]] = None,
        year_gt: Optional[int] = None,
        year_gte: Optional[int] = None,
        year_lt: Optional[int] = None,
        year_lte: Optional[int] = None,
        quarter: Optional[Union[int, list[int], "Series[int]"]] = None,
        refinery_id: Optional[Union[int, list[int], "Series[int]"]] = None,
        owner: Optional[Union[str, list[str], "Series[str]"]] = None,
        filter_exp: Optional[str] = None,
        skip: int = 0,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        """_summary_

        Parameters
        ----------
        year : Optional[Union[int, list[int], Series[int]]], optional
            filter by ``year = x`` , by default None
        year_gt : Optional[int], optional
            filter by ``year > x`` , by default None
        year_gte : Optional[int], optional
            filter by ``year >= x`` , by default None
        year_lt : Optional[int], optional
            filter by ``year < x`` , by default None
        year_lte : Optional[int], optional
            filter by ``year <= x`` , by default None
        quarter : Optional[Union[int, list[int], Series[int]]], optional
            filter by quarter, by default None
        refinery_id : Optional[Union[int, list[int], Series[int]]], optional
            filter by refineryId, by default None
        owner : Optional[Union[str, list[str], Series[str]]], optional
            filter by Owner/Name, by default None
        filter_exp : Optional[str], optional
            pass-thru ``$filter`` query param to use a handcrafted filter expression, by default None
        skip : int, optional
            pass-thru ``$skip`` query param to skip a certain number of records, by default 0
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default False
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
              DataFrame of the ``response.json()``
            Response
              Raw ``requests.Response`` object
        Examples
        --------
        **Simple**
        >>> WorldRefineryData().get_ownership(owner="BP")

        **Using Lists**
        >>> WorldRefineryData().get_ownership(year_gte=2017, quarter=[3, 4])

        **Using Series**
        >>> df = WorldRefineryData().get_reference_data(type=WorldRefineryData.RefTypes.Owners)
        >>> df = df[df['Name'].str.contains("Shell")]
        >>> WorldRefineryData().get_ownership(owner=df['Name'])
        """
        endpoint = "ownership"

        filter_params: list[str] = []

        filter_params.append(odata_list_to_filter("Year", year))
        filter_params.append(odata_list_to_filter("Quarter", quarter))
        filter_params.append(odata_list_to_filter("RefineryId", refinery_id))
        filter_params.append(odata_list_to_filter("Owner/Name", owner))

        if year_gt:
            filter_params.append(f"year gt {year_gt}")
        if year_gte:
            filter_params.append(f"year ge {year_gte}")
        if year_lt:
            filter_params.append(f"year lt {year_lt}")
        if year_lte:
            filter_params.append(f"year le {year_lte}")

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        else:
            filter_exp += " AND " + " AND ".join(filter_params)

        params = {
            "$skip": skip,
            "pageSize": page_size,
            "$count": "true",
            "$expand": "*",
        }

        if filter_exp:
            params["$filter"] = filter_exp

        # odata endpoint will not allow '+' character in URL seemingly
        qs = urlencode(params, quote_via=quote)

        return get_data(
            path=f"{self._endpoint}{endpoint}?{qs}",
            params={},
            # params=params,
            paginate=paginate,
            raw=raw,
            df_fn=self._to_df,
            paginate_fn=self._paginate,
        )

    def get_margins(
        self,
        *,
        date: Optional[Union[date, list[date], "Series[date]"]] = None,
        date_gt: Optional[date] = None,
        date_gte: Optional[date] = None,
        date_lt: Optional[date] = None,
        date_lte: Optional[date] = None,
        margin_type: Optional[Union[str, list[str], "Series[str]"]] = None,
        filter_exp: Optional[str] = None,
        skip: int = 0,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        """_summary_

        Parameters
        ----------
        date : Optional[Union[date, list[date], Series[date]]], optional
            filter by ``date = x`` , by default None
        date_gt : Optional[date], optional
            filter by ``date > x`` , by default None
        date_gte : Optional[date], optional
            filter by ``date >= x`` , by default None
        date_lt : Optional[date], optional
            filter by ``date < x`` , by default None
        date_lte : Optional[date], optional
            filter by ``date <= x`` , by default None
        margin_type : Optional[Union[str, list[str], Series[str]]], optional
            filter by MarginType/Name, by default None
        filter_exp : Optional[str], optional
            pass-thru ``$filter`` query param to use a handcrafted filter expression, by default None
        skip : int, optional
            pass-thru ``$skip`` query param to skip a certain number of records, by default 0
        page_size : int, optional
            pass-thru ``pageSize`` query param to request a particular page size, by default 1000
        paginate : bool, optional
            whether to auto-paginate the response, by default False
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
              DataFrame of the ``response.json()``
            Response
              Raw ``requests.Response`` object
        Examples
        --------
        **Simple**
        >>> WorldRefineryData().get_margins(date=date(2023, 2, 17))

        **Using Lists**
        >>> WorldRefineryData().get_margins(date_gte=date(2023, 1, 1), margin_type=['Dated Brent NWE Cracking', 'Dubai Singapore Cracking'])

        **Using Series**
        >>> df = WorldRefineryData().get_reference_data(type=WorldRefineryData.RefTypes.MarginTypes)
        >>> df = df[df['Name'].str.contains("Brent")]
        >>> WorldRefineryData().get_ownership(date_gte=date(2023, 1, 1), margin_type=df['Name'])
        """
        endpoint = "margins"

        filter_params: list[str] = []

        filter_params.append(odata_list_to_filter("Date", date))
        filter_params.append(odata_list_to_filter("MarginType/Name", margin_type))

        if date_gt:
            filter_params.append(f"Date gt {date_gt}")
        if date_gte:
            filter_params.append(f"Date ge {date_gte}")
        if date_lt:
            filter_params.append(f"Date lt {date_lt}")
        if date_lte:
            filter_params.append(f"Date le {date_lte}")

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        else:
            filter_exp += " AND " + " AND ".join(filter_params)

        params = {
            "$skip": skip,
            "pageSize": page_size,
            "$count": "true",
            "$expand": "*",
        }

        if filter_exp:
            params["$filter"] = filter_exp

        # odata endpoint will not allow '+' character in URL seemingly
        qs = urlencode(params, quote_via=quote)

        return get_data(
            path=f"{self._endpoint}{endpoint}?{qs}",
            params={},
            # params=params,
            paginate=paginate,
            raw=raw,
            df_fn=self._to_df,
            paginate_fn=self._paginate,
        )

    def get_reference_data(
        self, type: RefTypes, raw: bool = False
    ) -> Union[Response, DataFrame]:
        """
        Fetch reference data for the World Refinery Database.

        Parameters
        ----------
        type : RefTypes
            filter by type
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame``, by default False

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object
        Examples
        --------
        **Simple**
        >>> WorldRefineryData().get_reference_data(type=WorldRefineryData.RefTypes.Owners)
        """
        endpoint_path = type.value

        params = {"pageSize": 1000, "$skip": 0, "$expand": "*", "$count": "true"}

        if type == self.RefTypes.PADDs:
            df_fn = self._padd_to_df
        else:
            df_fn = self._to_df

        qs = urlencode(params, quote_via=quote)

        return get_data(
            path=f"{self._endpoint}{endpoint_path}?{qs}",
            params={},
            # params=params,
            paginate=True,
            raw=raw,
            paginate_fn=self._paginate,
            df_fn=df_fn,
        )
