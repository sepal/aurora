def get_rendered_votes_sum(sum):
    if sum == 0:
        return '[ ±0 ]'
    elif sum > 0:
        return '[ +' + str(sum) + ' ]'
    else:
        return '[ ' + str(sum) + ' ]'


def get_rendered_votes_sum_detailed(pos, neg):
    if pos == 0 and neg == 0:
        return '[ ±0 ]'
    else:
        return '[ +' + str(pos) + '-' + str(abs(neg)) + ' ]'
