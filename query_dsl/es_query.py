import click

import es_entities


@click.group('main')
@click.option('--es-host', type=str, default='http://localhost:9200', help='ES host.')
@click.option('--es-index', type=str, required=True, help='ES index name.')
@click.option('--limit', type=int, default=100, help='Limit number of entries in response.')
@click.pass_context
def main(ctx, es_host, es_index, limit):
    es_client = es_entities.Client(es_host, es_index, limit)
    ctx.obj = es_client


@main.command('fuzzy')
@click.option('--field', type=str, required=True, help='Field name to match.')
@click.option('--value', type=str, required=True, help='Field value to match.')
@click.pass_obj
def fuzzy(es_client, field, value):
    query = es_entities.Query().build(es_entities.QueryType.fuzzy, field, value)
    es_client.search(query)


@main.command('geo-distance')
@click.option('--geo-field', type=str, required=True, help='Field name with geo coordinates.')
@click.option('--distance', type=float, required=True, help='Distance from comparison location.')
@click.option('--distance-unit',
              type=click.Choice(['cm', 'm', 'km']),
              default='km',
              required=True,
              help='Distance measure unit.')
@click.option('--lat', type=float, required=True, help='Lat of location to compare.')
@click.option('--lon', type=float, required=True, help='Lon of location to compare.')
@click.pass_obj
def get_distance(es_client, geo_field, distance, distance_unit, lat, lon):
    query = es_entities.Query().build(es_entities.QueryType.geo_distance,
                                      geo_field,
                                      distance,
                                      distance_unit,
                                      lat,
                                      lon)
    es_client.search(query)


@main.command('match')
@click.option('--field', type=str, required=True, help='Field name to match.')
@click.option('--value', type=str, required=True, help='Field value to match.')
@click.pass_obj
def match(es_client, field, value):
    query = es_entities.Query().build(es_entities.QueryType.match, field, value)
    es_client.search(query)


@main.command('match-all')
@click.pass_obj
def match_all(es_client):
    query = es_entities.Query().build(es_entities.QueryType.match_all)
    es_client.search(query)


@main.command('multi-match')
@click.option('--field', '-f', type=str, required=True, multiple=True, help='Field name to match.')
@click.option('--value', type=str, required=True, help='Field value to match.')
@click.pass_obj
def multi_match(es_client, field, value):
    query = es_entities.Query().build(es_entities.QueryType.multi_match, field, value)
    es_client.search(query)


@main.command('term')
@click.option('--field', type=str, required=True, help='Field name to match.')
@click.option('--value', type=str, required=True, help='Field value to match.')
@click.pass_obj
def term(es_client, field, value):
    query = es_entities.Query().build(es_entities.QueryType.term, field, value)
    es_client.search(query)


@main.command('range')
@click.option('--field', type=str, required=True, help='Field name to match.')
@click.option('--gte', type=str, help='Greater or equal.')
@click.option('--gt', type=str, help='Strictly greater.')
@click.option('--lte', type=str, help='Less or equal.')
@click.option('--lt', type=str, help='Strictly less.')
@click.pass_obj
def range_q(es_client, field, gte, gt, lte, lt):
    if not any([gte, gt, lte, lt]):
        raise click.exceptions.UsageError('At least on of gte/gt/lte/lt has to be set.')
    query = es_entities.Query().build(es_entities.QueryType.range,
                                      field,
                                      dict(gte=gte, gt=gt, lte=lte, lt=lt))
    es_client.search(query)


if __name__ == '__main__':
    main()
