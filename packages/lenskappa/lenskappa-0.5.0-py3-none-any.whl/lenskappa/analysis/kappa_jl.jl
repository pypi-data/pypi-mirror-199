using DataFrames
using CSV
using StatsBase
using LinearAlgebra

function load_ms_weights(path::AbstractString)::DataFrame
    files = readdir(path, join=true)
    files = filter((x) -> endswith(x, ".csv"), files)
    nfiles = length(files)
    if nfiles != 64
        println("Expected 64 files but found $nfiles")
    end
    dfs = [DataFrame(CSV.File(path)) for path in files[1:4]]
    df = reduce(vcat, dfs)
end

function build_distribution(
    field_weight_path::String,
    weights::Vector{String},
    bins_per_dim::Int,
    lower_bound::Float64,
    upper_bound::Float64,
    )::StatsBase.Histogram
    field_weights = DataFrame(CSV.File(field_weight_path))
    selected_weights = field_weights[:, weights]
    bin_size = (upper_bound - lower_bound) / bins_per_dim
    vecs = Tuple(Vector(col) for col in eachcol(selected_weights))
    bins = lower_bound:bin_size:upper_bound
    hist = fit(StatsBase.Histogram, vecs, Tuple(bins for _ in 1:length(vecs)))
    hist = normalize(hist, mode=:density)
end

function normalize_ms_weights(ms_weights::DataFrame)
    for name in names(ms_weights)
        med_ = median(ms_weights[:,name])
        ms_weights[:,name] = ms_weights[:,name] / med_
    end
    ms_weights
end 


function partition_ms(
    ms_weights::DataFrame,
    edges::AbstractRange
    )
    indices = zeros(Int16, nrow(ms_weights), ncol(ms_weights))
    for (i, column) in enumerate(eachcol(ms_weights))
        partition = searchsortedfirst.(Ref(edges), column)
        indices[:,i] = partition
    end
    indices
end

function compute_pdfs(
    likelihood::StatsBase.Histogram,
    ms_partitions:: Matrix,
    kappas:: Array,
    kappa_bins:: AbstractRange,
    threads:: Int32 = 0,
)
a = 1
end