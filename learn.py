from datetime import datetime
from multiprocessing.pool import Pool

from models import Match, Agent, Chromosome


def get_score(agent):
    return agent.accuracy


def learn():
    while len(Chromosome.all()) < 30:
        Chromosome().create()
    test_set = Match.test_set()
    if not test_set:
        print('There are no matches to learn from')
        return
    agent_pool = [Agent(c) for c in Chromosome.all()]
    reserve = []
    n = 1
    with Pool(4) as pool:
        while True:
            try:
                print('Starting Generation {}'.format(n))
                start = datetime.now()
                for n2, agent in enumerate(agent_pool):
                    print('Running Agent {}'.format(n2))
                    guesses = pool.map(agent.guess, test_set)
                    agent.right = guesses.count(True)
                    agent.wrong = guesses.count(False)
                    agent.chromosome.agent_score = agent.accuracy
                    agent.chromosome.save()
                agent_pool.extend(reserve)
                agent_pool.sort(key=get_score, reverse=True)
                print('Generation took {}'.format(datetime.now() - start))
                print('Best Agent: {}% accurate'.format(agent_pool[0].accuracy * 100))
                Chromosome.delete_many(ids=[agent.chromosome.id for agent in agent_pool[15:]])
                agent_pool = [Agent(agent.chromosome.mutate()) for agent in agent_pool[:15]]  # mutate the top half
                reserve = agent_pool[:15]
                n += 1
            except KeyboardInterrupt:
                Chromosome.clean()  # keep best 15
                break
    print('Finished learning')


if __name__ == '__main__':
    learn()
