def get_rendered_votes_sum(sum):
    if sum == 0:
        return '[ ±0 ]'
    elif sum > 0:
        return '[ +' + str(sum) + ' ]'
    else:
        return '[ ' + str(sum) + ' ]'
