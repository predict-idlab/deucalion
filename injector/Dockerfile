# syntax=docker/dockerfile:1

FROM golang:1.19.2-alpine as build

WORKDIR /build

COPY go.mod ./
COPY go.sum ./

RUN go mod download

COPY deucalion-injector.go ./
COPY webhook/* ./webhook/
COPY manual/* ./manual/

RUN go build deucalion-injector.go

FROM alpine:latest
WORKDIR /app

COPY --from=build /build/deucalion-injector .

ENTRYPOINT ["./deucalion-injector"]
