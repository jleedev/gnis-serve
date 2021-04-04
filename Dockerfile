FROM debian:bullseye-slim AS builder

RUN apt-get update && \
	apt-get -y --no-install-recommends install \
		curl ca-certificates gdal-bin python3 && \
	apt-get clean

WORKDIR /build/
RUN curl -Of https://geonames.usgs.gov/docs/stategaz/NationalFile.zip
COPY update.py /build/
RUN python3 update.py > NationalFile.geojson
RUN ogr2ogr -t_srs wgs84 -s_srs epsg:4269 NationalFile.gpkg NationalFile.geojson

FROM gospatial/tegola
WORKDIR /data/
COPY --from=builder /build/NationalFile.gpkg /data/
COPY config.toml /data/

ENV PORT 8080
ENTRYPOINT []
CMD /opt/tegola serve --config /data/config.toml --port ":$PORT"

