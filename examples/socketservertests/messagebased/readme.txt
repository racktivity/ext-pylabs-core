the overhead of creating rpc messages (our own serialization and back) is quite heavy.
On my notebook I get end2end at +-750 roundtrips per second.
Id I disable the creation at both sides of the messageobjects I get to 2500 roundtrips per sec

@todo despiegk: I think we can do this much faster by not having to init a messageobject all the time and work on the way we serialize and deserialize, maybe json is also quite slow
