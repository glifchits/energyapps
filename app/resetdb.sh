#!/bin/bash
psql -c "drop schema public cascade; create schema public;" && python -c "import schema; schema.db.create_all(); print 'Database reset successful'"
