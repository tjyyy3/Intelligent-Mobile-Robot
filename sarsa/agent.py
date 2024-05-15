import math
import numpy as np


class SarsaAgent(object):
    def __init__(self,
                 obs_n,
                 act_n,
                 learning_rate=0.01,
                 gamma=0.9,
                 e_greed=0.9):
        self.act_n = act_n  # 动作维度，有几个动作可选
        self.lr = learning_rate
        self.gamma = gamma  # reward的衰减率
        self.Q = np.zeros((obs_n, act_n))
        self.sample_count = 0
        self.epsilon_start = e_greed
        self.epsilon_end = 0.01
        self.epsilon_decay = 400

    def sample(self, obs):
        self.sample_count += 1
        self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * \
                       math.exp(-1. * self.sample_count / self.epsilon_decay)
        if np.random.uniform(0, 1) < (1.0 - self.epsilon):  # 根据table的Q值选动作
            action = self.predict(obs)
        else:
            action = np.random.choice(self.act_n)  # 随机探索选取一个动作
        return action

    def predict(self, obs):
        # print(obs)
        Q_list = self.Q[obs, :]
        maxQ = np.max(Q_list)
        action_list = np.where(Q_list == maxQ)[0]  # maxQ可能对应多个action
        action = np.random.choice(action_list)
        return action

    def learn(self, obs, action, reward, next_obs, next_action, done):
        predict_Q = self.Q[obs, action]
        if done:
            target_Q = reward  # 没有下一个状态了
        else:
            target_Q = reward + self.gamma * self.Q[next_obs,
                                                    next_action]  # Sarsa
        self.Q[obs, action] += self.lr * (target_Q - predict_Q)
